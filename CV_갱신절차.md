# CV 갱신 절차 점검표

영문 CV 페이지를 고칠 때마다 이 순서대로 처리한다

## 1. 파일 위치

- 원본은 Claude artifact "Hyeongjin Kim"(https://claude.ai/artifact/WTGE4GsR2NqgDpkA1C8RHE)이다
- 공개 페이지는 GitHub Pages 주소 https://hyeongjinkim0208.github.io/ 이고 저장소는 hyeongjinkim0208/hyeongjinkim0208.github.io 이다
- Google Sites에는 공개 페이지 주소만 링크하고 내용은 따로 고치지 않는다
- 저장소 index.html 에서 `<!-- CV-BODY-START` 와 `<!-- CV-BODY-END -->` 사이는 원본 페이지 본문과 늘 같아야 한다
- 표시 바깥(문서 머리 부분, meta 설명, 끝 태그)은 저장소에서만 관리한다
- Working Papers 절만은 논문 상태 기록 `Dropbox/Research/working/_paper_status.json`(Research milestone 상황판이 읽는 파일)에서 `tools/build_working_papers.py` 로 만든다, 이 절은 손으로 고치지 않는다(7절)
- CV 쪽 반영 기록과 CV 표기 덮어쓰기는 `Dropbox/Research/working/_cv_entries.json` 에 둔다, 상태 파일은 여러 세션이 함께 고치므로 CV 작업에서는 읽기만 한다

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
- 연도 칸은 게재 연도, Forthcoming, Revise and resubmit, Submitted, In progress 중 하나로 쓴다
- 연구비는 지원 기관, 재원 부처, 과제번호를 함께 적는다(예: National Research Foundation of Korea (NRF), funded by the Ministry of Education · NRF-2023S1A5B5A19093456)
- 원고번호(manuscript number)는 CV에 넣지 않는다
- Working Papers 의 제목은 Title Case 로 적고, 학술지가 붙이는 접두어(JUE Insight: 등)와 국문 메모는 뺀다, 원고 제목이 다른 꼴이면 _cv_entries.json 의 overrides 에 CV 표기를 적는다

## 4. 논문 상태가 바뀔 때

- 아래 사건이 생기면 상태 파일의 그 원고 줄을 먼저 고친다(원고 폴더 세션의 CLAUDE.md 규칙), Working Papers 절은 거기서 자동으로 따라온다
  - 제목 확정이나 변경 → title(CV 표기가 다르면 _cv_entries.json 의 overrides 에 그 원고의 title)
  - 투고 → stage review, submitted_on, target_journal, 연도 칸은 Submitted, 설명은 "Submitted to (the) *학술지명*, 월 연도"
  - 수정 요청 → stage rr, 설명은 "Revise and resubmit, *학술지명*"
  - 채택 → stage accepted, 설명은 "*학술지명*, forthcoming"
  - 게재 → stage published, 스크립트가 Working Papers 에서 빼고 알려 주면 Journal Articles 로 손으로 옮기고 권, 호, 쪽수, DOI를 넣는다
  - 새 원고가 통합본에 이르면 cv.list 를 true 로 두어 In progress 로 올린다(설계 단계의 원고는 HJ 가 정함)
- 항목을 옮기거나 더하면 섹션 제목 옆 개수 표시도 함께 고친다(Working Papers 는 스크립트가 고침)

## 5. 반영 순서

- Working Papers 가 바뀔 때: 매일 아침 예약 작업("CV Working Papers 동기화")이 스크립트를 돌려 index.html, 원본 페이지, _cv_entries.json 을 함께 맞춘다, 급하면 같은 순서를 손으로 돌린다(`python3 tools/build_working_papers.py` → index.html 표시 사이 본문으로 원본 페이지 다시 게시 → _cv_entries.json 은 _bak 에 옛 판을 옮긴 뒤 새로 만듦)
- 다른 절이 바뀔 때: 원본 페이지를 고쳐 다시 게시하고, 게시한 본문 파일로 `python3 tools/sync_body.py <본문 파일>` 을 실행해 index.html 표시 사이를 교체한다
- `git diff` 로 의도한 줄만 바뀌었는지 확인한다
- 바뀐 내용을 한 줄로 적어 main에 커밋하고 push한다
- 1–2분 뒤 공개 주소에서 바뀐 항목이 보이는지 확인한다

## 6. 마무리 확인

- 왼쪽 "Last updated" 의 월을 고친 달로 맞춘다
- 섹션 개수 표시와 실제 항목 수가 같은지 본다
- 투고 원고, CV, 다른 문서 사이에 이름 철자나 과제번호가 다르게 적힌 곳이 있으면 알린다

## 7. Research milestone 연계

- 상태 파일의 원고 줄은 title, stage, target_journal, submitted_on 과 `cv` 칸(list, title, authors, journal)을 가진다, 원고 폴더 세션이 고치는 값이다
- `_cv_entries.json` 은 CV 쪽 기록이다: `overrides`(원고별 CV 표기, 있으면 상태 파일의 cv 칸 대신 씀), `synced`(CV 에 올린 제목, 상태, 학술지, 날짜, 스크립트가 적음), `changelog`
- 상태 파일의 cv.synced 는 2026-10-24 판의 흔적이다, _cv_entries.json 이 있으면 쓰지 않는다
- 상황판(Research milestone)은 상태 파일과 overrides 로 CV 에 나올 값을 계산해 synced 와 비교하고, 다르면 논문별 현황 표의 CV 열에 "갱신 필요"를 보인다, 다음 날 아침 예약 작업이 돌면 사라진다
- 스크립트 사용법: `--check` 는 고치지 않고 갱신이 필요한 줄만 보여 준다, `--status <경로>` 와 `--entries <경로>` 로 두 파일 위치를 바꾼다(기본 ~/Dropbox/Research/working/), `--html <파일>` 로 원본 페이지 본문 파일도 함께 고친다, `--no-mark` 는 HTML 만 고친다, `--today` 로 날짜를 정한다
- 순서 규칙: Forthcoming → Revise and resubmit → Submitted(투고일 늦은 것부터) → In progress(투고 준비 → 집필 → 분석 → 설계, 같으면 상태 파일 순서)
- 학술지 이름 앞의 "the" 는 Journal of, Review of, Annals of, Quarterly Journal, International Journal 로 시작할 때만 붙인다
- 데스크 리젝 뒤 다른 학술지로 옮기면 상태 파일의 target_journal 과 submitted_on 만 고치면 된다, overrides 에 옛 학술지가 남아 있으면 지운다

## 수정 이력

- 2026-10-17: 점검표 작성, index.html 에 본문 표시와 sync_body.py 추가
- 2026-10-24: Working Papers 절을 논문 상태 기록에서 만드는 tools/build_working_papers.py 추가, 1절·3절·4절·5절을 그에 맞춰 고치고 7절(Research milestone 연계)을 더함, 첫 실행으로 Economics Letters 와 Journal of Urban Economics 투고(2026-10-24)를 Submitted 로, ai words·firm productivity·investment rnd 의 제목을 현재 원고 제목으로, immigrant inflow 를 In progress 로 더함(8편 → 9편)
- 2026-10-29: 상태 파일이 바뀌어도 CV 가 따라오지 않던 문제를 고침, CV 반영 기록을 _cv_entries.json 으로 떼고 스크립트는 상태 파일을 읽기만 하게 바꿈, 매일 아침 예약 작업으로 동기화, 산업단지(JPubE 투고), 빵집 거리 제한(JUE 리젝 뒤 IJIO 투고, 새 제목), 자동화(새 제목)를 반영
