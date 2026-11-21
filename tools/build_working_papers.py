"""논문 상태 기록(_paper_status.json)에서 CV 의 Working Papers 절과 Work in Progress 절을 만들어 HTML 에 넣는다.

사용법
  python3 tools/build_working_papers.py                      # index.html 을 고치고 CV 반영 기록 파일에 반영 기록을 씀
  python3 tools/build_working_papers.py --check              # 고치지 않고 CV 갱신이 필요한 줄만 보여 줌
  python3 tools/build_working_papers.py --html <파일> ...    # 다른 HTML(원본 페이지 본문 파일 등)도 함께 고침
  python3 tools/build_working_papers.py --status <경로>      # 상태 파일 위치(기본 ~/Dropbox/Research/working/_paper_status.json), 읽기만 함
  python3 tools/build_working_papers.py --entries <경로>     # CV 반영 기록 파일 위치(기본 ~/Dropbox/Research/working/_cv_entries.json)
  python3 tools/build_working_papers.py --no-mark            # HTML 만 고치고 CV 반영 기록 파일은 건드리지 않음
  python3 tools/build_working_papers.py --backup-name <이름>  # 사본을 로컬에 만들지 않고 changelog 에 이 이름만 적음(GitHub 자동 반영용, 사본은 tools/dropbox_sync.py 가 Dropbox 에 만듦)

규칙(CV_갱신절차.md 4절, 7절)
  - 올릴지와 어느 절에 올릴지는 상태 파일의 stage, 원고 항목(milestones), events, authors 로 자동 판정함(2026-11-21)
    - Working Papers: stage 가 review, rr, accepted 이거나, 통합본이 done 이거나, events 에 투고 줄이 있는 원고(한 번 투고한 원고는 재구성 중이어도 내리지 않음)
    - Work in Progress: 위에 들지 않는 모든 원고(설계 단계와 저자 미정 포함, HJ 결정 2026-11-21 오전), 상태 파일에 줄이 있으면 오름
  - CV 표기 칸(hide, list, title, authors, journal)은 CV 반영 기록 파일의 overrides 에 그 원고가 있으면 그것, 없으면 상태 파일의 cv 칸을 씀
    - hide 가 true 면 판정과 상관없이 올리지 않음(끄기 스위치)
    - list 는 이제 쓰지 않음(true 든 false 든 판정을 따름)
    - 제목은 표기 칸의 title 이 있으면 그것, 없으면 상태 파일의 title
  - 연도 칸: review → Submitted, rr → Revise and resubmit, accepted → Forthcoming, Working Papers 의 그 밖(투고 전 초고)은 Draft, Work in Progress 는 In progress
  - review 라도 events 에 그 학술지의 "심사 시작"(또는 under review) 줄이 투고일 이후로 있으면 Under review(데스크를 지나 심사에 들어간 것)
  - published 는 Working Papers 에서 빼고 Journal Articles 로 손으로 옮기라고 알림
  - 설명 줄: Submitted 는 "Submitted to (the) <em>학술지</em>, 월 연도", Under review 는 "Under review at (the) <em>학술지</em>, submitted 월 연도", Revise and resubmit 와 Forthcoming 은 학술지만
  - 학술지 이름은 cv.journal 이 있으면 그것, 없으면 target_journal 에서 괄호 이하를 뗀 것
  - Working Papers 순서: Forthcoming → Revise and resubmit → Under review → Submitted(둘 다 투고일 늦은 것부터) → Draft(stage 가 투고에 가까운 것부터, 같으면 파일 순서)
  - Work in Progress 순서: stage 가 투고에 가까운 것부터, 같으면 파일 순서, 올릴 원고가 없으면 절과 목차 줄에 hidden 을 붙여 감춤
  - 반영 기록은 CV 반영 기록 파일의 synced 에 원고마다 CV 에 올린 제목, 상태, 학술지, 날짜로 적고 changelog 에 한 줄 더함, 상황판이 이 값과 상태 파일을 비교해 갱신 필요를 표시함
  - 2026-10-29 부터 상태 파일은 읽기만 하고 고치지 않음(여러 세션이 함께 고치는 파일이라), 상태 파일의 cv.synced 는 반영 기록 파일이 없을 때만 비교에 씀
  - CV 반영 기록 파일을 고치기 전에 같은 폴더 _bak/_cv_entries_YYMMDD_v<n>.json 사본을 둠
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
STATUS_RANK = {"Forthcoming": 0, "Revise and resubmit": 1, "Under review": 2, "Submitted": 3, "Draft": 4, "In progress": 5}
WITH_JOURNAL = ("Submitted", "Under review", "Revise and resubmit", "Forthcoming", "Published")
UNDER_REVIEW_WORDS = ("심사 시작", "under review")
STAGE_RANK = {"ready": 0, "drafting": 1, "analysis": 2, "design": 3, "unknown": 4}
THE_PREFIXES = ("Journal of", "Review of", "Annals of", "Quarterly Journal", "International Journal")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

SECTION_RE = re.compile(r'(<section class="section" id="working-papers">\n)(.*?)(\n      </section>)', re.S)
WIP_RE = re.compile(r'<section class="section" id="work-in-progress"(?: hidden)?>\n.*?\n      </section>', re.S)
NAV_WP_RE = re.compile(r'\n([ \t]*)<a href="#working-papers">.*?</a>')
NAV_WIP_RE = re.compile(r'<a href="#work-in-progress"(?: hidden)?>')
WIP_NOTE = "Projects in design, analysis, or drafting. Titles are tentative."
UPDATED_RE = re.compile(r'<p class="updated">Last updated [A-Z][a-z]+ \d{4}</p>')


def journal_name(p):
    cv = p.get("_cv") or {}
    if cv.get("journal"):
        return cv["journal"]
    j = (p.get("target_journal") or "").strip()
    return re.sub(r"\s*[\(（].*$", "", j).strip()


def plain_journal(name):
    return re.sub(r"\s*[\(（].*$", "", name or "").strip().casefold()


def under_review(p, journal):
    """stage 가 review 이고 events 에 그 학술지의 심사 시작 줄이 투고일 이후로 있으면 True"""
    if p.get("stage") != "review":
        return False
    since = p.get("submitted_on") or ""
    for ev in p.get("events") or []:
        text = f"{ev.get('event', '')} {ev.get('note', '')}".casefold()
        if not any(w in text for w in UNDER_REVIEW_WORDS):
            continue
        if plain_journal(ev.get("journal")) != plain_journal(journal):
            continue
        if (ev.get("date") or "") >= since:
            return True
    return False


def milestone(p, item):
    ms = p.get("milestones") or []
    if isinstance(ms, str):
        try:
            ms = json.loads(ms)
        except Exception:
            ms = []
    for m in ms:
        if m.get("item") == item:
            return m.get("state")
    return None


def ever_submitted(p):
    return any("투고" in (ev.get("event") or "") for ev in p.get("events") or [])


def placement(p):
    """올릴 절("wp" Working Papers, "wip" 그 밖의 모든 원고가 가는 Work in Progress, None 은 hide 로 감춘 원고)과 연도 칸의 상태"""
    cv = p.get("_cv") or {}
    if cv.get("hide"):
        return None, ""
    status = STATUS_BY_STAGE.get(p.get("stage"))
    if status:
        return "wp", status
    if milestone(p, "통합본") == "done" or ever_submitted(p):
        return "wp", "Draft"
    return "wip", "In progress"


def month_year(iso):
    try:
        d = dt.date.fromisoformat(iso)
    except Exception:
        return ""
    return f"{MONTHS[d.month - 1]} {d.year}"


def entry(p):
    cv = p.get("_cv") or {}
    title = (cv.get("title") or p["title"]).strip()
    section, status = placement(p)
    journal = journal_name(p) if status in WITH_JOURNAL else ""
    if status == "Submitted" and under_review(p, journal):
        status = "Under review"
    meta = ""
    the = "the " if journal.startswith(THE_PREFIXES) else ""
    when = month_year(p.get("submitted_on", ""))
    if status == "Submitted":
        meta = f"Submitted to {the}<em>{html.escape(journal)}</em>" + (f", {when}" if when else "")
    elif status == "Under review":
        meta = f"Under review at {the}<em>{html.escape(journal)}</em>" + (f", submitted {when}" if when else "")
    elif status == "Revise and resubmit":
        meta = f"Revise and resubmit, <em>{html.escape(journal)}</em>"
    elif status == "Forthcoming":
        meta = f"<em>{html.escape(journal)}</em>, forthcoming"
    return {"paper_id": p["paper_id"], "section": section, "title": title, "status": status, "journal": journal, "meta": meta,
            "authors": (cv.get("authors") or "").strip(), "submitted_on": p.get("submitted_on") or "",
            "stage": p.get("stage", "unknown")}


def sort_key(e, idx):
    return (STATUS_RANK.get(e["status"], 9),
            -(int(e["submitted_on"].replace("-", "")) if e["status"] in ("Submitted", "Under review") and e["submitted_on"] else 0),
            STAGE_RANK.get(e["stage"], 9) if e["status"] in ("Draft", "In progress") else 0,
            idx)


def render_rows(entries):
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
    return "".join(r + "\n" for r in rows)


def render(entries):
    """Working Papers 절의 안쪽(h2 와 목록)"""
    return (f'        <h2>Working Papers <span class="count">{len(entries)}</span></h2>\n'
            '        <div class="ledger">\n' + render_rows(entries) +
            '        </div>')


def render_wip(entries):
    """Work in Progress 절 전체, 올릴 원고가 없으면 hidden"""
    hidden = "" if entries else " hidden"
    return (f'<section class="section" id="work-in-progress"{hidden}>\n'
            f'        <h2>Work in Progress <span class="count">{len(entries)}</span></h2>\n'
            f'        <p class="note">{WIP_NOTE}</p>\n'
            '        <div class="ledger">\n' + render_rows(entries) +
            '        </div>\n'
            '      </section>')


def apply_html(path, section, wip_section, wip_shown, today):
    text = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(text)
    if not m:
        sys.exit(f"{path}: working-papers 절을 찾지 못함")
    new = text[:m.start(2)] + section + text[m.end(2):]
    w = WIP_RE.search(new)
    if w:
        new = new[:w.start()] + wip_section + new[w.end():]
    else:  # 절이 아직 없는 옛 본문: Working Papers 절 바로 뒤에 넣음
        m = SECTION_RE.search(new)
        new = new[:m.end()] + "\n\n      " + wip_section + new[m.end():]
    nav = f'<a href="#work-in-progress"{"" if wip_shown else " hidden"}>'
    if NAV_WIP_RE.search(new):
        new = NAV_WIP_RE.sub(nav, new, count=1)
    else:  # 목차 줄이 아직 없는 옛 본문: Working Papers 줄 바로 뒤에 넣음
        n = NAV_WP_RE.search(new)
        if n:
            new = new[:n.end()] + f'\n{n.group(1)}{nav}<span class="n"></span>Work in Progress</a>' + new[n.end():]
    if new != text:
        new = UPDATED_RE.sub(f'<p class="updated">Last updated {MONTHS[today.month - 1]} {today.year}</p>', new, count=1)
        path.write_text(new, encoding="utf-8")
        return True
    return False


def needs_update(p, e, synced):
    s = synced.get(p["paper_id"]) if synced is not None else ((p.get("cv") or {}).get("synced"))
    s = s or {}
    return not (s.get("title") == e["title"] and s.get("status") == e["status"] and (s.get("journal") or "") == e["journal"])


def backup(path, today):
    bak = path.parent / "_bak"
    bak.mkdir(exist_ok=True)
    stem = f"{path.stem}_{today:%y%m%d}_v"
    n = 1 + max([int(m.group(1)) for f in bak.glob(stem + "*.json") for m in [re.search(r"_v(\d+)\.json$", f.name)] if m] or [0])
    dest = bak / f"{stem}{n}.json"
    shutil.copy2(path, dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    base = pathlib.Path.home() / "Dropbox/Research/working"
    ap.add_argument("--status", default=str(base / "_paper_status.json"))
    ap.add_argument("--entries", default=str(base / "_cv_entries.json"))
    ap.add_argument("--html", nargs="*", default=None, help="고칠 HTML 파일, 기본은 저장소의 index.html")
    ap.add_argument("--check", action="store_true", help="고치지 않고 갱신이 필요한 줄만 보여 줌")
    ap.add_argument("--no-mark", action="store_true", help="CV 반영 기록 파일을 쓰지 않음")
    ap.add_argument("--today", default=None, help="날짜를 지정(YYYY-MM-DD), 기본은 오늘")
    ap.add_argument("--backup-name", default=None, help="CV 반영 기록 사본 이름(로컬 사본을 만들지 않음)")
    args = ap.parse_args()

    doc = json.loads(pathlib.Path(args.status).expanduser().read_text(encoding="utf-8"))
    entries_path = pathlib.Path(args.entries).expanduser()
    ent = json.loads(entries_path.read_text(encoding="utf-8")) if entries_path.exists() else None
    overrides = (ent or {}).get("overrides") or {}
    synced = (ent or {}).get("synced") if ent is not None else None
    if synced is None and ent is not None:
        synced = {}
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    for p in doc["papers"]:
        p["_cv"] = overrides.get(p["paper_id"], p.get("cv") or {})
    entries, unlisted = [], []
    for i, p in enumerate(doc["papers"]):
        e = entry(p)
        if not e["section"]:
            unlisted.append(e)
            continue
        e["_idx"] = i
        e["_needs"] = needs_update(p, e, synced)
        entries.append(e)
    published = [e for e in entries if e["status"] == "Published"]
    live = [e for e in entries if e["status"] != "Published"]
    shown = sorted([e for e in live if e["section"] == "wp"], key=lambda e: sort_key(e, e["_idx"]))
    shown_wip = sorted([e for e in live if e["section"] == "wip"], key=lambda e: sort_key(e, e["_idx"]))

    for e in entries:
        flag = "갱신 필요" if e["_needs"] else "반영됨"
        where = {"wp": "Working Papers", "wip": "Work in Progress"}[e["section"]]
        print(f"{flag:5s}  {e['paper_id']:15s}  {where:16s}  {e['status']:20s}  {e['title']}")
    for e in unlisted:
        print(f"목록 외  {e['paper_id']:15s}  {'':16s}  {'':20s}  {e['title']}")
    for e in published:
        print(f"알림  {e['paper_id']}: stage 가 published 라 Working Papers 에서 뺌, Journal Articles 에 권·호·쪽·DOI 와 함께 손으로 옮길 것(CV_갱신절차 4절)")
    if args.check:
        return

    section = render(shown)
    wip_section = render_wip(shown_wip)
    html_paths = [pathlib.Path(h) for h in args.html] if args.html else [pathlib.Path(__file__).resolve().parent.parent / "index.html"]
    changed = [str(h) for h in html_paths if apply_html(h, section, wip_section, bool(shown_wip), today)]
    print("HTML 고침: " + (", ".join(changed) if changed else "변경 없음"))

    if args.no_mark:
        return
    stamp = today.isoformat()
    ent = ent if ent is not None else {"_readme": [], "overrides": {}, "synced": {}, "changelog": []}
    ent.setdefault("synced", {})
    touched = []
    for e in entries:
        new = {"title": e["title"], "status": e["status"], "journal": e["journal"], "on": stamp}
        old = ent["synced"].get(e["paper_id"]) or {}
        if {k: old.get(k) for k in ("title", "status", "journal")} != {k: new[k] for k in ("title", "status", "journal")}:
            ent["synced"][e["paper_id"]] = new
            touched.append(e["paper_id"])
    gone = [k for k in ent["synced"] if k not in {e["paper_id"] for e in entries}]
    for k in gone:
        del ent["synced"][k]
    if not touched and not gone:
        print("CV 반영 기록: 변경 없음")
        return
    if args.backup_name:
        dest = pathlib.Path(args.backup_name)
    else:
        dest = backup(entries_path, today) if entries_path.exists() else None
    ent["updated"] = stamp
    ent.setdefault("changelog", []).append(
        f"{stamp}: Working Papers 절을 다시 만들고 synced 를 고침({', '.join(touched + gone)})"
        + (f", 고치기 전 판은 _bak/{dest.name}" if dest else ""))
    entries_path.write_text(json.dumps(ent, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"CV 반영 기록 고침: {len(touched)}줄 반영, {len(gone)}줄 삭제" + (f", 사본 {dest}" if dest else ""))


if __name__ == "__main__":
    main()
