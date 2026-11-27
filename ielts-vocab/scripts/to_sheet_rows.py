#!/usr/bin/env python3
"""Convert data/words.json (11/24 page) into rows matching the IELTS 단어 DB sheet (단어DB tab, A:X)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
extra = {  # 변형·파생어, 예문 해석
 "desperately": ("desperate; desperation", "그녀는 시험이 시작되기 전에 필사적으로 자리를 찾고 있었다."),
 "emigration": ("emigrate; emigrant", "1990년대에 농촌 지역에서의 해외 이주가 급증했다."),
 "cripple": ("crippling; crippled", "파업으로 도시 교통망이 마비되었다."),
 "slurp up": ("slurp", "아이들이 국수를 후루룩 먹었다."),
 "democratic": ("democracy; democratically", "모든 회원은 민주적인 투표권을 가진다."),
 "alignment": ("align; aligned", "그 정책은 국제 기준과 일치한다."),
 "naughty": ("naughtiness", "말썽꾸러기 소년이 누나의 신발을 숨겼다."),
 "chief": ("chiefly", "비용이 지연의 주된 이유였다."),
 "keynote": ("keynote speech; keynote speaker", "장관이 학회에서 기조연설을 했다."),
 "defecate": ("defecation", "어떤 동물들은 영역을 표시하려고 배변한다."),
 "urine": ("urinate; urinary", "의사가 소변 샘플을 요청했다."),
 "menstruation": ("menstruate; menstrual", "월경은 보통 10세에서 15세 사이에 시작된다."),
 "dysmenorrhoea": ("dysmenorrhea (US)", "생리통은 매달 많은 젊은 여성에게 영향을 준다."),
 "coercion": ("coerce; coercive", "그 자백은 강압에 의해 얻어졌다."),
 "refrain": ("refrained; refraining", "시험 중에는 휴대폰 사용을 삼가 주세요."),
 "invention": ("invent; inventor; inventive", "인쇄기는 혁신적인 발명품이었다."),
 "purpose": ("purposeful; purposely", "이 설문의 주된 목적은 무엇인가요?"),
 "depression": ("depress; depressed; depressing", "대공황은 약 10년간 지속되었다."),
 "resistance": ("resist; resistant", "새 시간표에 대한 반대가 거셌다."),
 "route": ("routes; routing", "그 버스 노선은 박물관을 지나간다."),
 "refreshments": ("refresh; refreshing", "다과는 11시에 강당에서 제공됩니다."),
 "cathedral": ("cathedrals", "투어는 12세기 대성당에서 끝난다."),
 "chapel": ("chapels", "병원 안에 작은 예배당이 있다."),
 "hang on": ("hold on", "잠깐만요, 예약 번호를 확인해 볼게요."),
 "except": ("exception; exceptional", "도서관은 일요일을 제외하고 매일 연다."),
 "verb": ("verbal; verbally", "determine은 동사이고 determination은 명사다."),
 "chase up": ("follow up", "늦은 배송 건은 제가 공급업체에 독촉할게요."),
 "stripping": ("strip; stripped", "줄기에서 껍질을 벗겨 내면 섬유가 나온다."),
 "resurgence": ("resurgent; resurge", "최근 몇 년간 대마 재배가 다시 늘고 있다."),
 "cellulose": ("cellulosic", "종이는 주로 셀룰로스로 만들어진다."),
 "emerging": ("emerge; emergence", "신흥 시장은 선진 시장보다 빠르게 성장하고 있다."),
 "prohibition": ("prohibit; prohibitive", "대마 재배 금지령은 1993년에 해제되었다."),
 "threatened": ("threaten; threat; threatening", "많은 멸종 위기종이 이 숲에만 산다."),
 "virtually": ("virtual", "그 질병은 사실상 사라졌다."),
 "hemp": ("hemp seed; hemp fibre", "대마는 농약 없이 재배할 수 있다."),
 "resistant": ("resist; resistance", "이 품종은 대부분의 해충에 강하다."),
 "dioxin": ("dioxins", "다이옥신은 연소 과정의 부산물이다."),
 "retardant": ("retard; retardation", "그 직물은 방염제로 처리되어 있다."),
 "fertiliser": ("fertilise; fertile; fertility", "대마는 면에 비해 비료가 적게 든다."),
 "require": ("requirement; required", "그 작물은 물이 아주 적게 필요하다."),
 "mild": ("mildly; mildness", "그 지역은 일 년 내내 기후가 온화하다."),
 "temperature": ("temperatures", "대마는 15~27°C에서 가장 잘 자란다."),
 "criticise": ("criticism; critic; critical", "그 보고서는 비용을 무시했다는 비판을 받았다."),
 "government": ("govern; governmental", "정부는 농업에 관한 새 규정을 도입했다."),
 "lumping": ("lump; lumped together", "대마를 마약 작물과 한데 묶은 것은 잘못이었다."),
 "determine": ("determination; determined", "토양의 질이 작물의 생장을 결정한다."),
 "relevant": ("relevance; irrelevant", "질문과 관련된 정보만 포함하세요."),
 "approximately": ("approximate; approximation", "토지의 약 40%가 농업에 쓰인다."),
}
PDF = "https://drive.google.com/file/d/1BCODXORl8eUaqRGZnZEuXL1GizQuBTPO/view"
rows = []
for i, w in enumerate(json.load(open(ROOT / "data/words.json")), 1):
    forms, exko = extra[w["word"]]
    memo = "; ".join(x for x in [w.get("note", ""), f"내가 쓴 철자: {w['wrong']}" if w.get("wrong") else ""] if x)
    rows.append([f"word-1124-{i}", w["word"], w["ko"], w.get("syn", ""), forms, w["ex"], exko,
                 w["section"], w["date"], "회사Drive Word.pdf p.2-3", str(i), w.get("wrong") or w["word"],
                 "", memo, "", "", 0, PDF, "", "", "", "", "GoodNotes/IELTS/Word.pdf (회사 Drive, 11/24 내보내기)", ""])
print(json.dumps(rows, ensure_ascii=False))
