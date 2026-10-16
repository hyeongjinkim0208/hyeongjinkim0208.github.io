# CV 갱신 절차 점검표

영문 CV 페이지를 고칠 때마다 이 순서대로 처리한다

## 1. 파일 위치

- 원본은 Claude artifact "Hyeongjin Kim"(https://claude.ai/artifact/WTGE4GsR2NqgDpkA1C8RHE)이다
- 공개 페이지는 GitHub Pages 주소 https://hyeongjinkim0208.github.io/ 이고 저장소는 hyeongjinkim0208/hyeongjinkim0208.github.io 이다
- Google Sites에는 공개 페이지 주소만 링크하고 내용은 따로 고치지 않는다
- 저장소 index.html 에서 `<!-- CV-BODY-START` 와 `<!-- CV-BODY-END -->` 사이는 원본 페이지 본문과 늘 같아야 한다
- 표시 바깥(문서 머리 부분, meta 설명, 끝 태그)은 저장소에서만 관리한다

## 2. 고치기 전 확인

- 원본 페이지 최신본을 먼저 읽는다
- 저장소를 받아 index.html 표시 사이 본문이 원본과 같은지 확인한다
- 둘이 다르면 어느 쪽이 최신인지 먼저 확인하고, 임의로 한쪽을 덮어쓰지 않는다
- 새로 넣을 사실(투고일, 학술지명, 과제번호, 쪽수, DOI)은 메일, 원고, 증빙 파일에서 확인한 값만 쓴다

## 3. 표기 기준

- About은 1인칭(I)으로 쓴다
- 학위는 미국식으로 적는다(공학 학사는 B.S.)
- 지도교수와 공저자 전봉걸은 "Bong Guel Chun"으로 적는다
- 국문 발표물은 영문 제목을 먼저 쓰고 국문 원제를 아래에 병기한다
- 위탁 기관은 실제 수행 센터가 아니라 상위 기관 약어로 적는다(LIMAC은 KRILA, LOMAC은 LOFA)
- 연도 칸은 게재 연도, Forthcoming, Submitted, In progress 중 하나로 쓴다
- 연구비는 지원 기관, 재원 부처, 과제번호를 함께 적는다(예: National Research Foundation of Korea (NRF), funded by the Ministry of Education · NRF-2023S1A5B5A19093456)
- 원고번호(manuscript number)는 CV에 넣지 않는다

## 4. 논문 상태가 바뀔 때

- 투고하면 Working Papers 맨 위로 올리고 연도 칸을 Submitted, 설명을 "Submitted to the *학술지명*, 월 연도"로 바꾼다
- 수정 요청을 받으면 설명을 "Revise and resubmit, *학술지명*"으로 바꾼다
- 게재가 확정되면 Journal Articles로 옮기고 권, 호, 쪽수, DOI를 넣는다
- 항목을 옮기거나 더하면 섹션 제목 옆 개수 표시도 함께 고친다

## 5. 반영 순서

- 원본 페이지를 고쳐 다시 게시한다
- 게시한 본문 파일로 `python3 tools/sync_body.py <본문 파일>` 을 실행해 index.html 표시 사이를 교체한다
- `git diff` 로 의도한 줄만 바뀌었는지 확인한다
- 바뀐 내용을 한 줄로 적어 main에 커밋하고 push한다
- 1–2분 뒤 공개 주소에서 바뀐 항목이 보이는지 확인한다

## 6. 마무리 확인

- 왼쪽 "Last updated" 의 월을 고친 달로 맞춘다
- 섹션 개수 표시와 실제 항목 수가 같은지 본다
- 투고 원고, CV, 다른 문서 사이에 이름 철자나 과제번호가 다르게 적힌 곳이 있으면 알린다

## 수정 이력

- 2026-10-17: 점검표 작성, index.html 에 본문 표시와 sync_body.py 추가
