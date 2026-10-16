"""원본 페이지(Claude artifact) 본문을 index.html 의 CV-BODY 표시 사이에 옮겨 넣는다.

사용법: python3 tools/sync_body.py <원본 페이지 본문 파일>

본문 파일은 <title>Hyeongjin Kim</title> 로 시작하는 HTML 이다.
Artifact read 로 받은 파일처럼 앞뒤에 플랫폼이 붙인 <html><head>...<body> 와
</body></html> 가 있어도 자동으로 떼어 낸다.
"""
import pathlib
import sys

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
    new = html[:s] + body + html[e:]
    if new == html:
        print("변경 없음")
        return
    index.write_text(new, encoding="utf-8")
    print("index.html 본문 교체 완료")


if __name__ == "__main__":
    main()
