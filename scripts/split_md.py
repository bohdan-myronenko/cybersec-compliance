import re, pathlib

raw = pathlib.Path("../kb/NIS2_Directive_Full_Text.md").read_text()
articles = re.split(r"(?=### Article\s+\d+)", raw)
for art in articles:
    m = re.match(r"### Article\s+(\d+)\s+[-–]?\s*(.*)", art)
    if not m:
        continue
    num, title = m.groups()
    text = art.strip()
    path = pathlib.Path(f"kb/nis2/article_{num}_{title.lower().replace(' ','_')}.md")
    path.write_text(text, encoding="utf-8")