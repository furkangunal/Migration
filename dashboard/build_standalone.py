"""index.html + data/ klasöründen, tarayıcıda tek başına açılan dashboard.html üretir.

Kullanım: python dashboard/build_standalone.py   (önce prep.py çalıştırılmalı)
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
DATA = D / "data"
PARAMS = {"a": "Turkey", "b": "Germany", "tab": "genel", "ulke": "Turkey", "yil": 2012}

datasets = {}
for f in sorted(DATA.iterdir()):
    if f.suffix == ".csv":
        datasets[f.stem] = {"format": "csv", "text": f.read_text(encoding="utf-8")}
    elif f.suffix == ".json":
        datasets[f.stem] = {"format": "json", "data": json.loads(f.read_text(encoding="utf-8"))}

def js(obj):
    # </script> dizisi gömülü veriyi erken kapatmasın
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

page = (D / "index.html").read_text(encoding="utf-8").replace('<meta name="dash-one-writer">', "", 1)
shim = (D / "dash_shim.js").read_text(encoding="utf-8")

# Panelin sağladığı tasarım değişkenlerinin karşılıkları
TOKENS = """
  :root {
    --font-anthropic-sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-anthropic-serif: Georgia, "Times New Roman", serif;
    --cds-font-size-caption: 0.78rem; --cds-font-size-body: 0.95rem;
    --cds-font-size-heading: 1.2rem; --cds-font-size-title: 1.55rem; --cds-font-weight-medium: 500;
    --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 14px; --cds-gap-lg: 22px;
    --cds-pad-md: 14px; --cds-pad-lg: 22px; --cds-pad-xl: 34px; --cds-radius: 10px;
    --cds-dur-slow: 400ms; --cds-ease-out: cubic-bezier(.2, .7, .3, 1);
    --color-fg: #0c2340; --color-fg-muted: #5b6b84; --color-bg: #f3f7fd; --color-panel: #ffffff;
    --color-border-line: #d8e2f0; --color-ok: #2e8b57; --color-warn: #d4a017; --color-bad: #c0392b;
  }
  html, body { margin: 0; background: #f3f7fd; }
  /* Panel gibi: hidden özniteliği sayfanın display kurallarını (.gp-page { display: grid }) ezsin */
  [hidden] { display: none !important; }
  .dash-skeleton { min-height: 160px; border-radius: var(--cds-radius);
    background: linear-gradient(90deg, #edf2f9 25%, #f7f9fd 50%, #edf2f9 75%); background-size: 200% 100%;
    animation: dash-shimmer 1.4s linear infinite; }
  @keyframes dash-shimmer { to { background-position: -200% 0; } }
"""

html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Küresel Göç Paneli</title>
<style>{TOKENS}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>window.DASH_DATA = {js(datasets)}; window.DASH_PARAMS = {js(PARAMS)};</script>
<script>
{shim}
</script>
</head>
<body>
<div id="dash-root">
{page}
</div>
<script>dash.__start();</script>
</body>
</html>
"""

out = D / "dashboard.html"
out.write_text(html, encoding="utf-8")
print(f"{out} yazıldı ({out.stat().st_size / 1024:.0f} KB, {len(datasets)} veri seti)")
