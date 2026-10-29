"""원본 페이지(Claude artifact) 본문을 index.html 의 CV-BODY 표시 사이에 옮겨 넣는다.

사용법: python3 tools/sync_body.py <원본 페이지 본문 파일>

본문 파일은 <title>Hyeongjin Kim</title> 로 시작하는 HTML 이다.
Artifact read 로 받은 파일처럼 앞뒤에 플랫폼이 붙인 <html><head>...<body> 와
</body></html> 가 있어도 자동으로 떼어 낸다.

Working Papers 절은 GitHub 자동 반영(tools/dropbox_sync.py)이 저장소에서 만드는 절이라
원본 페이지 쪽이 아니라 index.html 에 있던 것을 그대로 둔다, "Last updated" 는 둘 중 늦은 달을 쓴다.
"""
import pathlib
import re
import sys

SECTION_RE = re.compile(r'(<section class="section" id="working-papers">\n)(.*?)(\n      </section>)', re.S)
UPDATED_RE = re.compile(r'<p class="updated">Last updated ([A-Z][a-z]+) (\d{4})</p>')
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def keep_repo_parts(new: str, old: str) -> str:
    mo, mn = SECTION_RE.search(old), SECTION_RE.search(new)
    if mo and mn:
        new = new[:mn.start(2)] + mo.group(2) + new[mn.end(2):]
    uo, un = UPDATED_RE.search(old), UPDATED_RE.search(new)
    if uo and un:
        key = lambda m: (int(m.group(2)), MONTHS.index(m.group(1)) if m.group(1) in MONTHS else -1)
        if key(uo) > key(un):
            new = new[:un.start()] + uo.group(0) + new[un.end():]
    return new

START = "<!-- CV-BODY-START"
END = "<!-- CV-BODY-END -->"


def load_body(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    i = text.find("<title>Hyeongjin Kim</title>")
    if i < 0:
        sys.exit("본문 파일에 <title>Hyeongjin Kim</title> 이 없음")
    text = text[i:]
    j = text.rfind("</body>")
    if j >= 0:
        text = text[:j]
    return text.rstrip("\n") + "\n\n"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    body = load_body(pathlib.Path(sys.argv[1]))
    index = pathlib.Path(__file__).resolve().parent.parent / "index.html"
    html = index.read_text(encoding="utf-8")
    s = html.find(START)
    e = html.find(END)
    if s < 0 or e < 0 or e < s:
        sys.exit("index.html 에서 CV-BODY 표시를 찾지 못함")
    s = html.index("\n", s) + 1
    new = keep_repo_parts(html[:s] + body + html[e:], html)
    if new == html:
        print("변경 없음")
        return
    index.write_text(new, encoding="utf-8")
    print("index.html 본문 교체 완료")


if __name__ == "__main__":
    main()
