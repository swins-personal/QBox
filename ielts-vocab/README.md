# IELTS Word Box

굿노트 손글씨 단어장 → 정리 페이지(PDF) + 단어 DB(Google Sheets) + 폰 복습 앱.

| 무엇 | 어디 |
|---|---|
| 손글씨 원본 | Drive `GoodNotes/IELTS/Word.pdf` (id `1bXlIYhhmYoPGNXpBUUhtOmZH8APpRZ-j`) |
| 정리 페이지 PDF | Drive `목표_IELTS 7.0/단어장 정리본/` (folder id `1sJTvyqJFI5fttItHWbgrPnRbq-YpIWba`) |
| 단어 DB 시트 | Drive `목표_IELTS 7.0/IELTS 단어 DB` (id `1sV3efYXRIzzKHTFRWghZeUCfj7IPIveUfwgm3x808dk`) |
| 복습 앱 | https://claude.ai/artifact/2bYvsEUaRa7hmdtNeSfdJd (단어는 앱 DB `words` 컬렉션) |
| 원본 데이터 | `data/words.json` (이 저장소, 모든 곳의 기준) |

## 매일 처리 절차

1. `Word.pdf`를 내려받아 페이지별 이미지로 렌더링한다 (`pdftoppm -r 90 -png`).
2. 이미 처리한 날짜는 시트 `Page log` 탭에서 확인한다. 정리본 페이지(텍스트에 `IELTS Vocabulary`, `손글씨 페이지 정리본`)는 건너뛴다.
3. 새 손글씨 페이지의 단어를 읽는다.
   - 영역(Word test / Listening / Reading / Writing / Speaking / Extra)과 날짜를 페이지 머리에서 가져온다.
   - Word test: 검은 글씨 = 내가 쓴 철자(`wrong`), 빨간 글씨 = 정답(`word`).
   - 단어 옆 메모(`- almost - nearly`)는 `syn` 또는 `note`로 옮긴다.
   - 숙제, 이메일 같은 단어가 아닌 메모는 넣지 않는다.
   - 같은 날짜에 중복된 단어는 한 번만.
4. `data/words.json`에 새 항목을 추가한다 (id는 이어서 `w0049`...). 필드: `date, section, word, pos, ko, def, syn, ex, wrong, note`.
5. 정리 페이지 생성: `python3 scripts/build_page.py YYYY-MM-DD pages/YYYY-MM-DD.html && node scripts/to_pdf.js pages/YYYY-MM-DD.html pages/YYYY-MM-DD.pdf`
6. PDF를 정리본 폴더에 `IELTS 단어 정리_YYMMDD.pdf`로 업로드한다.
7. 시트 `Words` 탭 마지막 행 아래에 새 행을 추가하고 (Status `new`, Added = 오늘), `Page log`에 한 줄 추가한다.
8. 앱 DB `words` 컬렉션에 새 문서를 `ArtifactData` batch `set`으로 추가한다 (doc_id = id, 데이터는 id 제외). 앱은 다시 배포할 필요 없음.
9. 커밋하고 푸시한다.

## 굿노트에서 교체하기

정리본 PDF를 열고 공유 → GoodNotes로 보내기 → 기존 `Word` 노트에 "페이지로 삽입"을 고른 뒤, 손글씨 페이지를 지우거나 뒤로 옮긴다.
