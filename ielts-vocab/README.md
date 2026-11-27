# IELTS Word Box

굿노트 손글씨 단어장 → 정리 페이지(PDF) + 단어 DB(Google Sheets) + 폰 복습 앱.

| 무엇 | 어디 |
|---|---|
| 손글씨 원본 | Drive `GoodNotes/IELTS/Word.pdf` (id `1bXlIYhhmYoPGNXpBUUhtOmZH8APpRZ-j`) |
| 정리 페이지 PDF | Drive `목표_IELTS 7.0/단어장 정리본/` (folder id `1sJTvyqJFI5fttItHWbgrPnRbq-YpIWba`) |
| **단어 DB (유일한 기준)** | Google 시트 `IELTS 단어 DB` (id `1bZrU54WYy17DyGjA1PhxPoBhkW6yZpHqYgvmg3EHsC8`), 탭 `단어DB`, `처리기록` |
| 복습 앱 | https://claude.ai/artifact/2bYvsEUaRa7hmdtNeSfdJd (Google Sheets 커넥터로 시트를 직접 읽고 씀) |
| 11/24 페이지 원본 데이터 | `data/words.json` → `scripts/to_sheet_rows.py`로 시트 179~226행에 넣음 |

## 매일 처리 절차

1. `Word.pdf`를 내려받아 페이지별 이미지로 렌더링한다 (`pdftoppm -r 90 -png`).
2. 이미 처리한 날짜는 시트 `단어DB`의 학습일·원본 페이지와 `처리기록` 탭에서 확인한다. 정리본 페이지(텍스트에 `IELTS Vocabulary`, `손글씨 페이지 정리본`)는 건너뛴다.
3. 새 손글씨 페이지의 단어를 읽는다.
   - 영역(Word test / Listening / Reading / Writing / Speaking / Extra)과 날짜를 페이지 머리에서 가져온다.
   - Word test: 검은 글씨 = 내가 쓴 철자(`wrong`), 빨간 글씨 = 정답(`word`).
   - 단어 옆 메모(`- almost - nearly`)는 `syn` 또는 `note`로 옮긴다.
   - 숙제, 이메일 같은 단어가 아닌 메모는 넣지 않는다.
   - 같은 날짜에 중복된 단어는 한 번만.
4. 시트 `단어DB`의 마지막 행 아래에 새 행을 추가한다. 열: 단어ID, 단어, 뜻, 유사어·관련어, 변형·파생어, 예문, 예문 해석, 영역, 학습일, 원본 페이지, 원본 행, 손글씨 원문, 인지상태(빈칸), 수정·학습 메모, 마지막 복습일, 다음 복습일, 복습 횟수(0), 교체 PDF, 명사형, 동사형, 형용사형, 부사형, 자료 출처, 사진 분류.
5. (선택) 정리 페이지 생성: `python3 scripts/build_page.py YYYY-MM-DD pages/YYYY-MM-DD.html && node scripts/to_pdf.js pages/YYYY-MM-DD.html pages/YYYY-MM-DD.pdf`
6. PDF를 정리본 폴더에 `IELTS 단어 정리_YYMMDD.pdf`로 업로드한다.
7. `처리기록` 탭에 한 줄 남긴다. 앱은 시트를 바로 읽으므로 다시 배포할 필요 없음.

## 앱의 채점 규칙

- 몰라요 = 인지상태 0, 애매해요 = 5, 알아요 = 이전 값 +3 (처음이면 7, 최대 10).
- 다음 복습일: 인지 0–4 → 1일, 5–6 → 2일, 7–8 → 4일, 9 → 7일, 10 → 14일 (이미 10이었으면 30일).
- 채점할 때마다 시트 M(인지상태), O(마지막 복습일), P(다음 복습일), Q(복습 횟수)에 쓴다. 쓰기 전에 A열의 단어ID로 행이 맞는지 확인한다.

## 굿노트에서 교체하기

정리본 PDF를 열고 공유 → GoodNotes로 보내기 → 기존 `Word` 노트에 "페이지로 삽입"을 고른 뒤, 손글씨 페이지를 지우거나 뒤로 옮긴다.
