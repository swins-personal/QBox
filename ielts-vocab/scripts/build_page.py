#!/usr/bin/env python3
"""Build a clean A4 vocabulary page (HTML) for one study date from data/words.json.
Usage: build_page.py YYYY-MM-DD out.html"""
import json, sys, html, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
date, out = sys.argv[1], sys.argv[2]
words = [w for w in json.load(open(ROOT / "data/words.json")) if w["date"] == date]
order = ["Word test", "Listening", "Reading", "Writing", "Speaking", "Extra"]
label = {"Word test": "Spelling test", "Extra": "Word family"}
d = datetime.date.fromisoformat(date)
e = html.escape

secs = []
n = 0
for s in order:
    ws = [w for w in words if w["section"] == s]
    if not ws:
        continue
    rows = []
    for w in ws:
        n += 1
        meta = []
        if w.get("syn"):
            meta.append(f'<span class="tag">≈</span> {e(w["syn"])}')
        if w.get("wrong"):
            meta.append(f'<span class="tag x">✗</span> <s>{e(w["wrong"])}</s>')
        if w.get("note"):
            meta.append(f'<span class="tag">✎</span> {e(w["note"])}')
        rows.append(f'''<div class="row">
  <div class="no">{n:02d}</div>
  <div class="w"><b>{e(w["word"])}</b><i>{e(w["pos"])}</i></div>
  <div class="m"><div class="ko">{e(w["ko"])}</div>
    {'<div class="meta">' + ' &nbsp;·&nbsp; '.join(meta) + '</div>' if meta else ''}
    <div class="ex">{e(w["ex"])}</div></div>
  <div class="chk"><span></span><span></span><span></span></div>
</div>''')
    secs.append(f'<section><h2>{e(label.get(s, s))}<em>{len(ws)}</em></h2>{"".join(rows)}</section>')

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css" rel="stylesheet">
<style>
@page {{ size: A4; margin: 14mm 13mm 14mm 13mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Pretendard, sans-serif; color: #1d2433; font-size: 8.8pt; line-height: 1.3; }}
header {{ display: flex; align-items: flex-end; justify-content: space-between;
  border-bottom: 2.2pt solid #1fbf84; padding-bottom: 3mm; margin-bottom: 4mm; }}
header h1 {{ font-size: 20pt; letter-spacing: -.3pt; font-weight: 800; }}
header h1 span {{ color: #1fbf84; }}
header .r {{ text-align: right; color: #667085; font-size: 8.5pt; }}
header .r b {{ display: block; font-size: 13pt; color: #1d2433; }}
section {{ margin-bottom: 4mm; }}
h2 {{ font-size: 10pt; font-weight: 800; text-transform: uppercase; letter-spacing: .8pt; color: #0e8f61;
  background: #e8f8f1; padding: 1.2mm 2.5mm; border-radius: 1.5mm; margin-bottom: 1mm; break-after: avoid; }}
h2 em {{ font-style: normal; color: #667085; font-weight: 600; margin-left: 2mm; }}
.row {{ display: grid; grid-template-columns: 7mm 42mm 1fr 13mm; gap: 2.5mm; padding: 1.1mm 1mm;
  border-bottom: .5pt solid #e4e7ec; break-inside: avoid; }}
.no {{ color: #98a2b3; font-size: 8pt; padding-top: .6mm; font-variant-numeric: tabular-nums; }}
.w b {{ display: block; font-size: 10.5pt; font-weight: 700; letter-spacing: -.1pt; }}
.w i {{ font-style: normal; color: #1fbf84; font-size: 8pt; font-weight: 600; }}
.ko {{ font-weight: 600; }}
.meta {{ color: #475467; font-size: 8.3pt; }}
.meta s {{ color: #d0465b; }}
.tag {{ color: #98a2b3; font-weight: 700; }}
.tag.x {{ color: #d0465b; }}
.ex {{ color: #667085; font-style: italic; font-size: 8.3pt; }}
.chk {{ display: flex; gap: 1.2mm; padding-top: 1mm; }}
.chk span {{ width: 3mm; height: 3mm; border: .7pt solid #c4cad4; border-radius: 50%; }}
footer {{ margin-top: 3mm; color: #98a2b3; font-size: 7.5pt; text-align: right; }}
</style></head><body>
<header><h1>IELTS <span>Vocabulary</span></h1>
<div class="r"><b>{d.strftime("%y/%m/%d")} ({"월화수목금토일"[d.weekday()]})</b>{n} words · ◯◯◯ = 복습 체크</div></header>
{"".join(secs)}
<footer>Target 7.0 · 손글씨 페이지 정리본</footer>
</body></html>'''
open(out, "w").write(page)
print(out, n)
