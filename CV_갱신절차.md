# CV 갱신 절차 점검표

영문 CV 페이지를 고칠 때마다 이 순서대로 처리한다

## 1. 파일 위치

- 원본은 Claude artifact "Hyeongjin Kim"(https://claude.ai/artifact/WTGE4GsR2NqgDpkA1C8RHE)이다
- 공개 페이지는 GitHub Pages 주소 https://hyeongjinkim0208.github.io/ 이고 저장소는 hyeongjinkim0208/hyeongjinkim0208.github.io 이다
- Google Sites에는 공개 페이지 주소만 링크하고 내용은 따로 고치지 않는다
- 저장소 index.html 에서 `<!-- CV-BODY-START` 와 `<!-- CV-BODY-END -->` 사이는 원본 페이지 본문과 늘 같아야 한다, 예외는 Working Papers 절, Work in Progress 절(목차 줄의 hidden 포함), "Last updated" 줄로 저장소 쪽이 앞설 수 있다(7절)
- 표시 바깥(문서 머리 부분, meta 설명, 끝 태그)은 저장소에서만 관리한다
- Working Papers 절과 Work in Progress 절은 논문 상태 기록 `Dropbox/Research/working/_paper_status.json`(Research milestone 상황판이 읽는 파일)에서 `tools/build_working_papers.py` 로 만든다, 두 절은 손으로 고치지 않는다(7절)
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
- 연도 칸은 게재 연도, Forthcoming, Revise and resubmit, Under review, Submitted, Draft(Working Papers 의 투고 전 초고), In progress(Work in Progress 절) 중 하나로 쓴다
- 연구비는 지원 기관, 재원 부처, 과제번호를 함께 적는다(예: National Research Foundation of Korea (NRF), funded by the Ministry of Education · NRF-2023S1A5B5A19093456)
- 원고번호(manuscript number)는 CV에 넣지 않는다
- MRTC 발간물은 연구원 시리즈 이름으로 적는다: MRTC Research Report Series(연구보고서, Basic 은 붙이지 않음), MRTC Policy Report Series(정책보고서), MRTC Working Paper Series(워킹페이퍼), 브리프는 MRTC Issue Brief, MRTC Statistics Brief, MRTC Brief (Issue) 그대로
- MRTC 발간물에는 시리즈 이름 뒤에 발간번호를 "No. 2025-09" 꼴로 붙인다, 번호는 연구원 누리집 발간물 상세 화면의 발간번호나 발간본 파일 이름에서 확인한 값만 쓰고 과제 폴더 번호(R9, R11 등)는 발간번호와 다를 수 있으니 그대로 옮기지 않는다(2024년 이민과 경제(I)는 폴더 24-R9, 발간번호 2024-03), 발간 전 과제는 HJ 가 알려 준 번호를 쓴다
- MRTC 발간물의 국문 원제는 연구원 누리집 발간물 상세 화면의 제목에 맞춘다, 띄어쓰기도 그대로 옮기고 부제 앞에만 쌍점을 둔다, 새 발간물을 올릴 때는 상세 화면에서 발간번호, 제목, 저자를 한 번에 확인한다, 원제의 낱말이 바뀌어 뜻이 달라지면 영문 제목도 같이 고친다
- Policy Research Reports 의 저자 표시는 HJ 의 역할에 따라 셋으로 적는다: HJ 가 연구책임(PM, 1저자)이고 공동 저자가 있으면 "with 이름"으로 공동 저자를 적고, HJ 단독이면 아무 표시도 하지 않으며, HJ 가 공동연구진으로 참여한 과제에만 co-authored 를 붙인다, 역할과 공동 저자는 발간된 것은 누리집 상세 화면의 저자(책임, 공동), 발간 전인 것은 평가본 원고 표지(수탁 과제는 제출문)의 연구책임자와 공동연구자로 확인한다, 착수 단계 계획서는 최종 연구진과 다를 수 있어 쓰지 않는다, 연구보조원과 조사수행기관은 적지 않고, 영문 이름은 평가본 표지의 표기를 쓰며 표기가 없으면 본인이 쓰는 표기를 확인해 적는다
- Journal Articles 와 Policy Research Reports 절 머리에는 설명 글을 두지 않는다(HJ 결정 2026-11-24)
- Working Papers 와 Work in Progress 의 제목은 Title Case 로 적고, 학술지가 붙이는 접두어(JUE Insight: 등)와 국문 메모는 뺀다, 원고 제목이 다른 꼴이면 _cv_entries.json 의 overrides 에 CV 표기를 적는다, 가제인 원고는 내부 약칭이 아니라 주제가 드러나는 짧은 제목을 같은 자리에 적는다(Work in Progress 절 머리에 제목이 잠정이라는 안내가 있음)

## 4. 논문 상태가 바뀔 때

- 아래 사건이 생기면 상태 파일의 그 원고 줄을 먼저 고친다(원고 폴더 세션의 CLAUDE.md 규칙), Working Papers 절과 Work in Progress 절은 거기서 자동으로 따라온다
  - 제목 확정이나 변경 → title(CV 표기가 다르면 _cv_entries.json 의 overrides 에 그 원고의 title)
  - 투고 → stage review, submitted_on, target_journal, 연도 칸은 Submitted, 설명은 "Submitted to (the) *학술지명*, 월 연도"
  - 심사 시작(데스크 통과) → stage 는 review 그대로 두고 events 에 그 학술지의 "심사 시작" 줄(날짜, 저널)을 더한다, 연도 칸은 Under review, 설명은 "Under review at (the) *학술지명*, submitted 월 연도"
  - 수정 요청 → stage rr, 설명은 "Revise and resubmit, *학술지명*"
  - 채택 → stage accepted, 설명은 "*학술지명*, forthcoming"
  - 게재 → stage published, 스크립트가 Working Papers 에서 빼고 알려 주면 Journal Articles 로 손으로 옮기고 권, 호, 쪽수, DOI를 넣는다
  - 상태 파일에 원고 줄이 생기면(설계 단계, 저자 미정 포함) → Work in Progress 절에 In progress 로 자동으로 오른다, 저자 줄이 없으면 단독으로 읽히므로 공저가 정해지면 _cv_entries.json 의 overrides 에 그 원고의 authors("with ...")를 적는다
  - 통합본(원고 항목 7번)이 done 이 되면 → Working Papers 절로 옮겨 가고 연도 칸은 Draft
  - 원고마다 CV 등재 여부를 따로 묻거나 cv.list 를 고칠 필요가 없다(2026-11-21), 일부러 감추려면(보류한 원고 등) _cv_entries.json 의 overrides 에 그 원고의 hide 를 true 로 적는다, list 는 쓰지 않는다
- 항목을 옮기거나 더하면 섹션 제목 옆 개수 표시도 함께 고친다(Working Papers 와 Work in Progress 는 스크립트가 고침)

## 5. 반영 순서

- Working Papers 나 Work in Progress 가 바뀔 때: 할 일이 없다, 상태 파일만 고치면 GitHub 자동 반영이 10–20분 안에 공개 페이지를 고치고, 원본 페이지는 Claude 안에서 열 때 Dropbox 에서 바로 다시 그린다(7절), 급하면 GitHub 저장소 Actions 탭의 Sync Working Papers 에서 Run workflow 를 누른다
- 다른 절이 바뀔 때: 원본 페이지를 고쳐 다시 게시하고, 게시한 본문 파일로 `python3 tools/sync_body.py <본문 파일>` 을 실행해 index.html 표시 사이를 교체한다, 이때 Working Papers 절과 Work in Progress 절은 index.html 에 있던 것을 그대로 두고 "Last updated" 는 늦은 달을 쓴다
- 원본 페이지를 다시 게시할 때는 capabilities 를 빼고 게시해 Dropbox 읽기 설정(mcp: Dropbox fetch)을 그대로 둔다
- `git diff` 로 의도한 줄만 바뀌었는지 확인한다
- 바뀐 내용을 한 줄로 적어 main에 커밋하고 push한다
- 1–2분 뒤 공개 주소에서 바뀐 항목이 보이는지 확인한다

## 6. 마무리 확인

- 왼쪽 "Last updated" 의 월을 고친 달로 맞춘다
- 섹션 개수 표시와 실제 항목 수가 같은지 본다
- 투고 원고, CV, 다른 문서 사이에 이름 철자나 과제번호가 다르게 적힌 곳이 있으면 알린다

## 7. Research milestone 연계

- 상태 파일의 원고 줄은 title, authors, stage, target_journal, submitted_on, milestones, events 와 `cv` 칸(hide, title, authors, journal)을 가진다, 원고 폴더 세션이 고치는 값이다
- 등재 판정(2026-11-21): 먼저 hide 가 true 면 올리지 않는다, stage 가 review, rr, accepted 이거나 통합본이 done 이거나 events 에 투고 줄이 있으면 Working Papers(한 번 투고한 원고는 재구성으로 통합본이 partial 로 돌아가도 내리지 않는다), 그 밖의 원고는 모두 Work in Progress(설계 단계와 저자 미정 포함, 같은 날 오전 HJ 결정으로 설계 확정과 저자 조건을 없앰), cv.list 는 true 든 false 든 쓰지 않는다
- 등재 규칙의 글은 이 문서 4절과 7절에만 둔다, _cv_entries.json 의 _readme 에는 옮겨 적지 않고 이 문서를 가리키게 한다(규칙이 바뀔 때 고칠 곳을 줄임)
- Work in Progress 에 올릴 원고가 없으면 스크립트가 그 절과 목차 줄에 hidden 을 붙여 감춘다, 목차 번호는 CSS 카운터라 감춘 줄을 건너뛴다
- `_cv_entries.json` 은 CV 쪽 기록이다: `overrides`(원고별 CV 표기와 hide, 있으면 상태 파일의 cv 칸 대신 씀), `synced`(CV 에 올린 제목, 상태, 학술지, 날짜, 스크립트가 적음), `changelog`
- 상태 파일의 cv.synced 는 2026-10-24 판의 흔적이다, _cv_entries.json 이 있으면 쓰지 않는다
- 상황판(Research milestone)은 상태 파일과 overrides 로 CV 에 나올 값을 계산해 synced 와 비교하고, 다르면 논문별 현황 표의 CV 열에 "갱신 필요"를 보인다, 자동 반영이 돌면 10–20분 안에 사라지고, 한 시간 넘게 남아 있으면 자동 반영이 멈춘 것이다
- GitHub 자동 반영: `.github/workflows/sync-working-papers.yml` 이 10분마다 `tools/dropbox_sync.py` 를 돌린다, Dropbox API 로 두 파일을 받아 스크립트를 돌리고, index.html 이 바뀌면 커밋해 push 하고, synced 가 바뀌면 Dropbox 의 옛 판을 `_bak/_cv_entries_YYMMDD_v<n>.json` 으로 복사한 뒤 덮어쓴다(받은 뒤 누가 고쳤으면 덮어쓰지 않고 다음 회차에 다시 함)
- 자동 반영에 쓰는 열쇠는 저장소 Settings → Secrets and variables → Actions 의 DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN 이다, Dropbox 앱 이름은 hj-cv-sync
- 자동 반영이 실패하면 GitHub 이 메일로 알린다, 저장소에 60일 동안 커밋이 없으면 GitHub 이 예약 실행을 멈추므로 그런 메일이 오면 Actions 탭에서 다시 켠다
- 원본 페이지(artifact)의 Working Papers 절과 Work in Progress 절은 Claude 안에서 열면 Dropbox 의 두 파일을 읽어 같은 규칙으로 다시 그린다, 처음 열 때 Dropbox 사용을 묻는다, Claude 밖이나 공개 페이지에서는 저장된 정적 목록을 보인다
- 스크립트 사용법: `--check` 는 고치지 않고 갱신이 필요한 줄만 보여 준다, `--status <경로>` 와 `--entries <경로>` 로 두 파일 위치를 바꾼다(기본 ~/Dropbox/Research/working/), `--html <파일>` 로 원본 페이지 본문 파일도 함께 고친다, `--no-mark` 는 HTML 만 고친다, `--today` 로 날짜를 정한다
- 순서 규칙: Working Papers 는 Forthcoming → Revise and resubmit → Under review → Submitted(둘 다 투고일 늦은 것부터) → Draft, Draft 와 Work in Progress 안에서는 stage 순(투고 준비 → 집필 → 분석 → 설계, 같으면 상태 파일 순서)
- 등재 판정과 Under review 판정은 스크립트(placement, under_review), 원본 페이지와 index.html 의 실시간 스크립트(place, underReview), 상황판의 CV 열(cv_sync)이 같은 규칙으로 한다(Under review 는 stage review, events 의 event 나 note 에 "심사 시작" 또는 "under review", 저널명이 target_journal 과 같고 날짜가 submitted_on 이후), 셋 중 하나만 고치면 CV 열에 갱신 필요가 계속 남는다
- 학술지 이름 앞의 "the" 는 Journal of, Review of, Annals of, Quarterly Journal, International Journal 로 시작할 때만 붙인다
- 데스크 리젝 뒤 다른 학술지로 옮기면 상태 파일의 target_journal 과 submitted_on 만 고치면 된다, overrides 에 옛 학술지가 남아 있으면 지운다

## 수정 이력

- 2026-10-17: 점검표 작성, index.html 에 본문 표시와 sync_body.py 추가
- 2026-10-24: Working Papers 절을 논문 상태 기록에서 만드는 tools/build_working_papers.py 추가, 1절·3절·4절·5절을 그에 맞춰 고치고 7절(Research milestone 연계)을 더함, 첫 실행으로 Economics Letters 와 Journal of Urban Economics 투고(2026-10-24)를 Submitted 로, ai words·firm productivity·investment rnd 의 제목을 현재 원고 제목으로, immigrant inflow 를 In progress 로 더함(8편 → 9편)
- 2026-10-29: 상태 파일이 바뀌어도 CV 가 따라오지 않던 문제를 고침, CV 반영 기록을 _cv_entries.json 으로 떼고 스크립트는 상태 파일을 읽기만 하게 바꿈, 산업단지(JPubE 투고), 빵집 거리 제한(JUE 리젝 뒤 IJIO 투고, 새 제목), 자동화(새 제목)를 반영
- 2026-10-29(오후): GitHub 자동 반영(10분마다)을 더하고, 원본 페이지 Working Papers 절은 Dropbox 에서 바로 그리게 함, sync_body.py 는 Working Papers 절을 저장소 쪽으로 둠, 1절, 5절, 7절 고침
- 2026-11-03: 연도 칸에 Under review 를 더함(심사 시작 event 로 판정, 스크립트·원본 페이지·상황판 CV 열에 같이 반영), About 에 연구 흐름 문단(지역·재정 → 이민 → IO 와 측정)을 더함, 3절, 4절, 7절 고침
- 2026-11-21: CV 등재를 자동 판정으로 바꾸고 Work in Progress 절을 더함(HJ 결정: 설계 확정과 저자 결정이면 Work in Progress, 통합본이면 Working Papers, 투고 전 초고의 연도 칸은 Draft), cv.list 는 미리 올리는 스위치로만 남기고 hide 를 더함, 목차 번호를 CSS 카운터로 바꿈, 스크립트·실시간 스크립트·상황판 CV 열·sync_body.py 에 같이 반영, 1절, 3절, 4절, 5절, 7절 고침, 첫 실행으로 auto·firm productivity·investment rnd 는 Draft, manuprotection 은 Work in Progress 로 옮기고 factory thresholds 를 Work in Progress 에 더함
- 2026-11-21(오전, 두 번째): 설계 단계와 저자 미정 원고도 Work in Progress 에 올리기로 함(HJ 결정), 설계 확정과 저자 조건, list 스위치를 없애고 hide 만 남김, 절 머리 안내를 design 포함으로 고침, fireworks 와 reallocation 을 Work in Progress 에 더함(2편 → 4편), firm productivity 의 새 제목 반영, 4절, 7절 고침
- 2026-11-22: About 을 HJ 가 준 글로 바꿈(네 문단, 첫 문단은 큰 글씨 머리 문단), 칩을 Research fields(Public Economics, Urban and Regional Economics, Labor Economics)와 Research interests(Place-based Policy, Immigration, Firm Behavior) 두 줄로 나눔
- 2026-11-24: Policy Research Reports 절의 MRTC 발간물 표기를 연구원 시리즈 이름으로 맞춤(MRTC Basic Research Report 9건 → MRTC Research Report Series, MRTC Policy Report → MRTC Policy Report Series, MRTC Working Paper → MRTC Working Paper Series), 3절에 표기 기준을 더함
- 2026-11-24(두 번째): MRTC 발간물 14건에 발간번호를 붙임, 2026년 5건(연구보고서 2026-05, 2026-13, 2026-11, 2026-17, 브리프 2026-02)은 HJ 가 알려 준 값, 2024–2025년 9건은 연구원 누리집 발간물 화면과 발간본 파일 이름으로 확인(연구보고서 2025-09, 2025-10, 2025-02, 2024-03, 2024-07, 정책보고서 2024-02, 이슈브리프 2024-06, 워킹페이퍼 2024-01, 통계브리프 2024-07), 3절에 번호 기준을 더함
- 2026-11-24(세 번째): MRTC 발간물의 국문 원제와 공저 표시를 연구원 누리집 등록 내용에 맞춤, 원제 7건(2025-10 외국인주민 집중거주지역, 2025-02 국내 외국인 유학생, 2024-07 돌봄서비스 외국인력 정책 전망, 2024-02 정책보고서 연구개발에 미치는 영향과 향후 과제, 2024-03 이민과 경제(I), 통계브리프 2024-07 등록 공장과 연도 괄호 앞 빈칸, 브리프 2026-02 두뇌유출), 공저 표시 2건(연구보고서 2025-09 공동 소준영, 정책보고서 2024-02 공동 전봉걸), 돌봄 보고서 영문 제목에서 Introducing 을 뺌, 국민연금 추납 브리프(2026-03)는 누리집 브리프 목록 첫 화면에 없어 그대로 둠, 3절에 기준을 더함
- 2026-11-24(네 번째): Policy Research Reports 의 저자 표시를 HJ 의 역할로 나눔(HJ 결정: PM 과제는 with 이름, 참여 과제는 co-authored), 연구보고서 2025-09 는 with Junyoung So, 정책보고서 2024-02 는 with Bong Guel Chun 으로 바꾸고 연구보고서 2026-05 에 with Heonjae Song 을 더함(연구사업계획서의 공동연구 기준), PM 과제인 연구보고서 2026-13(공동 최서리, 송헌재, 강덕수)과 법무부 수탁 외국인 유입 적정규모(공동연구원 12인)는 영문 표기와 적는 방식을 HJ 에게 확인한 뒤 반영하기로 함, 3절 기준을 고침
- 2026-11-24(다섯 번째): 평가본 원고 표지로 연구진을 다시 확인함, 연구보고서 2026-05 는 HJ 단독이라 with Heonjae Song 을 지우고(착수 단계 계획서의 공동연구는 최종 연구진과 달랐음), 2026-13 에 with Seori Choi, Heonjae Song, and Deoksoo Kang 을 더하고, 법무부 수탁 외국인 유입 적정규모에는 제출문의 공동연구원 10인을 모두 적음(조사수행기관 케이스탯리서치와 연구보조원은 적지 않음, 영문 표기 가운데 평가본과 공개 자료로 확인한 것은 Seori Choi, Chang Won Lee, Seunghoon Han 이고 나머지는 HJ 확인 대기), Journal Articles 와 Policy Research Reports 절 머리 설명 글을 뺌(HJ 결정), 3절 기준을 고침
