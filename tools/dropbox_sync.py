"""GitHub Actions 에서 Dropbox 의 논문 상태 기록을 읽어 CV 의 Working Papers 절을 맞춘다.

사용법(.github/workflows/sync-working-papers.yml 이 부름)
  python3 tools/dropbox_sync.py pull <작업 폴더>   # 두 파일을 받아 build_working_papers.py 를 돌림, index.html 이 바뀔 수 있음
  python3 tools/dropbox_sync.py push <작업 폴더>   # CV 반영 기록이 바뀌었으면 Dropbox 의 옛 판을 _bak 에 복사하고 새 판을 올림

환경 변수(GitHub 저장소 Secrets): DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN

규칙
  - _paper_status.json 은 읽기만 함
  - _cv_entries.json 은 받은 판(rev)에서 바뀌지 않았을 때만 덮어씀, 그사이 누가 고쳤으면 이번 회차는 멈추고 다음 회차에 다시 함
  - 옛 판 사본은 /Research/working/_bak/_cv_entries_YYMMDD_v<n>.json (Asia/Seoul 날짜)
"""
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ROOT = "/Research/working"
STATUS = f"{ROOT}/_paper_status.json"
ENTRIES = f"{ROOT}/_cv_entries.json"
BAK = f"{ROOT}/_bak"
REPO = pathlib.Path(__file__).resolve().parent.parent


def token():
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
        "client_id": os.environ["DROPBOX_APP_KEY"],
        "client_secret": os.environ["DROPBOX_APP_SECRET"],
    }).encode()
    with urllib.request.urlopen("https://api.dropbox.com/oauth2/token", data=data, timeout=30) as r:
        return json.load(r)["access_token"]


def rpc(tok, endpoint, body):
    req = urllib.request.Request(f"https://api.dropboxapi.com/2/{endpoint}", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Dropbox {endpoint} 실패 {e.code}: {e.read().decode(errors='replace')[:500]}")


def download(tok, path):
    req = urllib.request.Request("https://content.dropboxapi.com/2/files/download", data=b"",
                                 headers={"Authorization": f"Bearer {tok}", "Dropbox-API-Arg": json.dumps({"path": path})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read(), json.loads(r.headers["Dropbox-API-Result"])
    except urllib.error.HTTPError as e:
        sys.exit(f"Dropbox 내려받기 실패 {path} {e.code}: {e.read().decode(errors='replace')[:500]}")


def upload(tok, path, content, rev):
    arg = {"path": path, "mode": {".tag": "update", "update": rev}, "autorename": False, "mute": True}
    req = urllib.request.Request("https://content.dropboxapi.com/2/files/upload", data=content,
                                 headers={"Authorization": f"Bearer {tok}", "Dropbox-API-Arg": json.dumps(arg),
                                          "Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Dropbox 올리기 실패 {e.code}: {e.read().decode(errors='replace')[:500]}")


def next_backup_name(tok, today):
    res = rpc(tok, "files/list_folder", {"path": BAK})
    names = [x["name"] for x in res["entries"]]
    while res.get("has_more"):
        res = rpc(tok, "files/list_folder/continue", {"cursor": res["cursor"]})
        names += [x["name"] for x in res["entries"]]
    stem = f"_cv_entries_{today:%y%m%d}_v"
    ns = [int(m.group(1)) for n in names for m in [re.fullmatch(re.escape(stem) + r"(\d+)\.json", n)] if m]
    return f"{stem}{max(ns or [0]) + 1}.json"


def pull(work):
    work.mkdir(parents=True, exist_ok=True)
    today = dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    tok = token()
    status, _ = download(tok, STATUS)
    entries, meta = download(tok, ENTRIES)
    (work / "status.json").write_bytes(status)
    (work / "_cv_entries.json").write_bytes(entries)
    json.loads(status)
    json.loads(entries)
    bak = next_backup_name(tok, today)
    state = {"entries_rev": meta["rev"], "backup_name": bak, "today": today.isoformat()}
    (work / "state.json").write_text(json.dumps(state))
    subprocess.run([sys.executable, str(REPO / "tools/build_working_papers.py"),
                    "--status", str(work / "status.json"), "--entries", str(work / "_cv_entries.json"),
                    "--today", today.isoformat(), "--backup-name", f"_bak/{bak}"], check=True)
    changed = (work / "_cv_entries.json").read_bytes() != entries
    (work / "entries_changed").write_text("1" if changed else "0")
    print("CV 반영 기록: " + ("바뀜, push 단계에서 Dropbox 에 올림" if changed else "변경 없음"))


def push(work):
    if (work / "entries_changed").read_text() != "1":
        print("Dropbox 에 올릴 것 없음")
        return
    state = json.loads((work / "state.json").read_text())
    tok = token()
    rpc(tok, "files/copy_v2", {"from_path": ENTRIES, "to_path": f"{BAK}/{state['backup_name']}", "autorename": False})
    res = upload(tok, ENTRIES, (work / "_cv_entries.json").read_bytes(), state["entries_rev"])
    print(f"Dropbox 고침: {res['path_display']} ({res['size']} bytes), 옛 판 {BAK}/{state['backup_name']}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("pull", "push"):
        sys.exit(__doc__)
    missing = [k for k in ("DROPBOX_APP_KEY", "DROPBOX_APP_SECRET", "DROPBOX_REFRESH_TOKEN") if not os.environ.get(k)]
    if missing:
        print("::warning::Dropbox 열쇠가 저장소 Secrets 에 없어 이번 회차를 건너뜀: " + ", ".join(missing))
        sys.exit(0)
    {"pull": pull, "push": push}[sys.argv[1]](pathlib.Path(sys.argv[2]))
