"""논문 상태 기록(_paper_status.json)에서 CV 의 Working Papers 절을 만들어 HTML 에 넣는다.

사용법
  python3 tools/build_working_papers.py                      # index.html 을 고치고 상태 파일에 반영 기록을 씀
  python3 tools/build_working_papers.py --check              # 고치지 않고 CV 갱신이 필요한 줄만 보여 줌
  python3 tools/build_working_papers.py --html <파일> ...    # 다른 HTML(원본 페이지 본문 파일 등)도 함께 고침
  python3 tools/build_working_papers.py --status <경로>      # 상태 파일 위치를 바꿈(기본 ~/Dropbox/Research/working/_paper_status.json)
  python3 tools/build_working_papers.py --no-mark            # HTML 만 고치고 상태 파일은 건드리지 않음

규칙(CV_갱신절차.md 4절, 7절)
  - cv.list 가 true 인 원고만 올림, 제목은 cv.title 이 있으면 그것, 없으면 title
  - 연도 칸은 stage 로 정함: review → Submitted, rr → Revise and resubmit, accepted → Forthcoming, 그 밖은 In progress
  - published 는 Working Papers 에서 빼고 Journal Articles 로 손으로 옮기라고 알림
  - 설명 줄: Submitted 는 "Submitted to (the) <em>학술지</em>, 월 연도", Revise and resubmit 와 Forthcoming 은 학술지만
  - 학술지 이름은 cv.journal 이 있으면 그것, 없으면 target_journal 에서 괄호 이하를 뗀 것
  - 순서: Forthcoming → Revise and resubmit → Submitted(투고일 늦은 것부터) → In progress(stage 가 투고에 가까운 것부터, 같으면 파일 순서)
  - --mark 이면 상태 파일의 cv.synced 에 CV 에 올린 제목, 상태, 학술지, 날짜를 적고 changelog 에 한 줄 더함, 상황판이 이 값과 title·stage 를 비교해 갱신 필요를 표시함
  - 상태 파일을 고치기 전에 _bak/_paper_status_YYMMDD_v<n>.json 사본을 둠(그 파일의 _readme 규칙)
"""
import argparse
import datetime as dt
import html
import json
import pathlib
import re
import shutil
import sys

STATUS_BY_STAGE = {"review": "Submitted", "rr": "Revise and resubmit", "accepted": "Forthcoming", "published": "Published"}
STATUS_RANK = {"Forthcoming": 0, "Revise and resubmit": 1, "Submitted": 2, "In progress": 3}
STAGE_RANK = {"ready": 0, "drafting": 1, "analysis": 2, "design": 3, "unknown": 4}
THE_PREFIXES = ("Journal of", "Review of", "Annals of", "Quarterly Journal")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

SECTION_RE = re.compile(r'(<section class="section" id="working-papers">\n)(.*?)(\n      </section>)', re.S)
UPDATED_RE = re.compile(r'<p class="updated">Last updated [A-Z][a-z]+ \d{4}</p>')


def journal_name(p):
    cv = p.get("cv") or {}
    if cv.get("journal"):
        return cv["journal"]
    j = (p.get("target_journal") or "").strip()
    return re.sub(r"\s*[\(（].*$", "", j).strip()


def month_year(iso):
    try:
        d = dt.date.fromisoformat(iso)
    except Exception:
        return ""
    return f"{MONTHS[d.month - 1]} {d.year}"


def entry(p):
    cv = p.get("cv") or {}
    title = (cv.get("title") or p["title"]).strip()
    status = STATUS_BY_STAGE.get(p.get("stage"), "In progress")
    journal = journal_name(p) if status != "In progress" else ""
    meta = ""
    if status == "Submitted":
        the = "the " if journal.startswith(THE_PREFIXES) else ""
        when = month_year(p.get("submitted_on", ""))
        meta = f"Submitted to {the}<em>{html.escape(journal)}</em>" + (f", {when}" if when else "")
    elif status == "Revise and resubmit":
        meta = f"Revise and resubmit, <em>{html.escape(journal)}</em>"
    elif status == "Forthcoming":
        meta = f"<em>{html.escape(journal)}</em>, forthcoming"
    return {"paper_id": p["paper_id"], "title": title, "status": status, "journal": journal, "meta": meta,
            "authors": (cv.get("authors") or "").strip(), "submitted_on": p.get("submitted_on") or "",
            "stage": p.get("stage", "unknown")}


def sort_key(e, idx):
    return (STATUS_RANK.get(e["status"], 9),
            -(int(e["submitted_on"].replace("-", "")) if e["status"] == "Submitted" and e["submitted_on"] else 0),
            STAGE_RANK.get(e["stage"], 9) if e["status"] == "In progress" else 0,
            idx)


def render(entries):
    rows = []
    for e in entries:
        b = [f'              <p class="t">{html.escape(e["title"], quote=False)}</p>']
        if e["authors"]:
            b.append(f'              <p class="auth">{html.escape(e["authors"], quote=False)}</p>')
        if e["meta"]:
            b.append(f'              <p class="meta">{e["meta"]}</p>')
        rows.append('          <div class="row">\n'
                    f'            <div class="y">{e["status"]}</div>\n'
                    '            <div class="b">\n' + "\n".join(b) + '\n'
                    '            </div>\n'
                    '          </div>')
    return (f'        <h2>Working Papers <span class="count">{len(entries)}</span></h2>\n'
            '        <div class="ledger">\n' + "\n".join(rows) + '\n'
            '        </div>')


def apply_html(path, section, today):
    text = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(text)
    if not m:
        sys.exit(f"{path}: working-papers 절을 찾지 못함")
    new = text[:m.start(2)] + section + text[m.end(2):]
    if new != text:
        new = UPDATED_RE.sub(f'<p class="updated">Last updated {MONTHS[today.month - 1]} {today.year}</p>', new, count=1)
        path.write_text(new, encoding="utf-8")
        return True
    return False


def needs_update(p, e):
    s = ((p.get("cv") or {}).get("synced")) or {}
    return not (s.get("title") == e["title"] and s.get("status") == e["status"] and (s.get("journal") or "") == e["journal"])


def dump_status(doc):
    """상태 파일의 손 편집 형식(윗단 1칸 들여쓰기, 원고 한 줄씩)을 그대로 지킨다."""
    j = lambda v: json.dumps(v, ensure_ascii=False)
    lines = ["{"]
    keys = list(doc.keys())
    for k in keys:
        v = doc[k]
        comma = "," if k != keys[-1] else ""
        if k == "papers":
            lines.append(' "papers": [')
            for i, p in enumerate(v):
                lines.append("  " + j(p) + ("," if i < len(v) - 1 else ""))
            lines.append(" ]" + comma)
        else:
            lines.append(f" {j(k)}: {j(v)}{comma}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def backup(status_path, today):
    bak = status_path.parent / "_bak"
    bak.mkdir(exist_ok=True)
    stem = f"_paper_status_{today:%y%m%d}_v"
    n = 1 + max([int(m.group(1)) for f in bak.glob(stem + "*.json") for m in [re.search(r"_v(\d+)\.json$", f.name)] if m] or [0])
    dest = bak / f"{stem}{n}.json"
    shutil.copy2(status_path, dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--status", default=str(pathlib.Path.home() / "Dropbox/Research/working/_paper_status.json"))
    ap.add_argument("--html", nargs="*", default=None, help="고칠 HTML 파일, 기본은 저장소의 index.html")
    ap.add_argument("--check", action="store_true", help="고치지 않고 갱신이 필요한 줄만 보여 줌")
    ap.add_argument("--no-mark", action="store_true", help="상태 파일의 cv.synced 를 쓰지 않음")
    args = ap.parse_args()

    status_path = pathlib.Path(args.status).expanduser()
    raw = status_path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    today = dt.date.today()

    listed = [(i, p) for i, p in enumerate(doc["papers"]) if (p.get("cv") or {}).get("list")]
    entries = []
    for i, p in listed:
        e = entry(p)
        e["_idx"] = i
        e["_needs"] = needs_update(p, e)
        entries.append(e)
    published = [e for e in entries if e["status"] == "Published"]
    shown = sorted([e for e in entries if e["status"] != "Published"], key=lambda e: sort_key(e, e["_idx"]))

    for e in entries:
        flag = "갱신 필요" if e["_needs"] else "반영됨"
        print(f"{flag:5s}  {e['paper_id']:9s}  {e['status']:20s}  {e['title']}")
    for e in published:
        print(f"알림  {e['paper_id']}: stage 가 published 라 Working Papers 에서 뺌, Journal Articles 에 권·호·쪽·DOI 와 함께 손으로 옮길 것(CV_갱신절차 4절)")
    if args.check:
        return

    section = render(shown)
    html_paths = [pathlib.Path(h) for h in args.html] if args.html else [pathlib.Path(__file__).resolve().parent.parent / "index.html"]
    changed = [str(h) for h in html_paths if apply_html(h, section, today)]
    print("HTML 고침: " + (", ".join(changed) if changed else "변경 없음"))

    if args.no_mark:
        return
    stamp = today.isoformat()
    touched = []
    for e in entries:
        p = doc["papers"][e["_idx"]]
        synced = {"title": e["title"], "status": e["status"], "journal": e["journal"], "on": stamp}
        if (p.get("cv") or {}).get("synced") != synced:
            p.setdefault("cv", {})["synced"] = synced
            touched.append(e["paper_id"])
    if not touched:
        print("상태 파일: cv.synced 변경 없음")
        return
    dest = backup(status_path, today)
    doc["updated"] = stamp
    doc.setdefault("changelog", []).append(
        f"{stamp}: CV Working Papers 절을 tools/build_working_papers.py 로 다시 만들고 cv.synced 를 적음({', '.join(touched)}), "
        f"고치기 전 판은 Research/working/_bak/{dest.name}")
    status_path.write_text(dump_status(doc), encoding="utf-8")
    print(f"상태 파일 고침: cv.synced {len(touched)}줄, 사본 {dest}")


if __name__ == "__main__":
    main()
