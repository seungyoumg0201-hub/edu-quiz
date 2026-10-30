# 오답 로그 (교육학 퀴즈 앱)

파일명: YYYY-MM-DD.txt (받은 날짜, KST). 사용자가 앱의 "오답 보내기"로 보낸 한 줄 텍스트를 그대로 저장.

형식: EDUWR1 {JSON}
- v: 1, d: 앱 기준 날짜, ts: epoch ms, n: 문항 수
- it[]: {id: 문항 id(final.json items.id), n: 오답 누적(st.wr), c/w: 정답/오답 횟수(st.hist), q: 앞면 60자, a: 최근 서술 답안 200자(있을 때), m: 놓친 핵심어}

수신 경로: 앱 메일 버튼 -> hsybot@mail.grokbot.com (제목 "교육학 오답로그 날짜") 또는 채팅 붙여넣기/파일.
야간 검토: 자정 이후 새 로그를 읽어 id별로 앞면 누설·모호함·답 구조를 점검하고 v4 소스에서 개선.

## v18 계정 동기화 (2026-10-30 추가)
- 백엔드: 전공퀴즈(geo-vocab)와 같은 Firebase 프로젝트 `geo-vocab`, 같은 Google 로그인. 공개 클라이언트 설정만 앱에 포함(비밀키 없음).
- 저장 위치(Realtime DB, 기존 보안규칙 안에서 동작 — 규칙 변경 없음):
  - `review/<uid>/devices/eduquiz` : 교육학 전체 진도 `p`(edu_quiz_v1 JSON 문자열), `wrN`, `seen`. 지리 데이터와 키가 겹치지 않음.
  - `review/<uid>/misses/*` 중 `d:"edu"` : 오답 1건마다 이벤트 {at,id,k,area,q,n,lv}. 지리 오답(d≠edu)과 같은 목록에 섞여 있으니 d로 구분.
- 앱 사용법: 상단 오른쪽 "로그인" 칩(🌙 옆) 탭 또는 📊 통계 > "☁️ 계정 동기화" > "Google로 로그인". 첫 로그인 때 이 기기의 기존 오답이 계정에 합쳐지고(삭제 없음) 백필 업로드됨.
- 박스 가져오기: `python3 /workspace/edu/wrong_log/pull.py` → `YYYY-MM-DD.json`, `latest.json`. 공개 읽기라 자격증명 불필요. uid 기본값 snw9XbdP1Xbf0Z3o0ISkTusAhdB3(이 DB의 유일한 사용자 = 전공앱 계정) — 다르면 `EDU_UID=... python3 pull.py`. 데이터 없으면 종료코드 2, 파일 안 만듦.
- 대체 경로: 위 EDUWR1 "오답 보내기" 버튼은 현재 앱에 없음. 대신 📊 통계 > 설정 > "학습 기록 백업(복사)" 내용을 hsybot@mail.grokbot.com으로 보내거나 채팅에 붙여넣기.
