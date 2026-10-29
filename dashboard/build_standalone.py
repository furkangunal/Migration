"""index.html + data/ klasöründen, tarayıcıda tek başına açılan iki dosya üretir:
dashboard.html (Türkçe) ve dashboard_en.html (İngilizce). Başlıktaki TR | EN düğmesi ikisi arasında geçer.

Kullanım: python dashboard/build_standalone.py   (önce prep.py çalıştırılmalı)
"""
import csv
import io
import json
from pathlib import Path

from i18n_en import PAGE, VALUES

D = Path(__file__).resolve().parent
DATA = D / "data"
PARAMS = {"a": "Turkey", "b": "Germany", "tab": "genel", "ulke": "Turkey", "yil": 2012}
FILES = {"tr": "dashboard.html", "en": "dashboard_en.html"}
TITLES = {"tr": "Küresel Göç Paneli", "en": "Global Migration Dashboard"}


def load_datasets():
    out = {}
    for f in sorted(DATA.iterdir()):
        if f.suffix == ".csv":
            out[f.stem] = {"format": "csv", "text": f.read_text(encoding="utf-8")}
        elif f.suffix == ".json":
            out[f.stem] = {"format": "json", "data": json.loads(f.read_text(encoding="utf-8"))}
    return out


def translate_csv(text):
    rows = list(csv.reader(io.StringIO(text)))
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows([[VALUES.get(c, c) for c in r] for r in rows])
    return buf.getvalue()


def translate_page(page):
    # Sınıf adları sayfada da geçer (lejantlar, data-where, renk tabloları); "Dünya" yalnızca PAGE'deki tırnaklı haliyle
    pairs = {**{k: v for k, v in VALUES.items() if k != "Dünya"}, **PAGE}
    missing = [k for k in PAGE if k not in page]
    if missing:
        raise SystemExit("index.html'de bulunamayan çeviri metinleri:\n  " + "\n  ".join(missing))
    for k in sorted(pairs, key=len, reverse=True):
        page = page.replace(k, pairs[k])
    return page


def js(obj):
    # </script> dizisi gömülü veriyi erken kapatmasın
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


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
  .gp-head .gp-wrap { position: relative; }
  .lang-switch { position: absolute; top: 0; right: max(16px, 2.5vw); display: flex; gap: 2px;
    border: 1px solid rgba(255, 255, 255, .35); border-radius: 999px; padding: 2px; font-size: .78rem; }
  .lang-switch a { color: #e3ecfa; text-decoration: none; padding: 3px 10px; border-radius: 999px; letter-spacing: .04em; }
  .lang-switch a:hover { color: #ffffff; }
  .lang-switch a[aria-current] { background: #ffffff; color: #0b3a82; font-weight: 600; }
"""


def switch(lang):
    links = []
    for code in ("tr", "en"):
        cur = ' aria-current="page"' if code == lang else ""
        links.append(f'<a href="{FILES[code]}" hreflang="{code}" lang="{code}"{cur}>{code.upper()}</a>')
    label = "Dil" if lang == "tr" else "Language"
    return f'<nav class="lang-switch" aria-label="{label}">{"".join(links)}</nav>'


# Dil değiştirirken açık sekmeyi koru
KEEP_TAB = """
document.querySelectorAll('.lang-switch a').forEach((a) => a.addEventListener('click', () => {
  a.href = a.getAttribute('href').split('#')[0] + '#' + (dash.params().tab || 'genel');
}));
// #sekme adı aynı id'li bölüme atlatmasın: sayfa başlıktan açılsın
if (location.hash) addEventListener('load', () => setTimeout(() => scrollTo(0, 0)));
"""


def build(lang, page, datasets, shim):
    head = '<header class="gp-head">\n    <div class="gp-wrap">'
    assert head in page, "index.html başlık yapısı değişmiş"
    page = page.replace(head, head + "\n      " + switch(lang), 1)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLES[lang]}</title>
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
<script>{KEEP_TAB}dash.__start();</script>
</body>
</html>
"""


page_tr = (D / "index.html").read_text(encoding="utf-8").replace('<meta name="dash-one-writer">', "", 1)
shim = (D / "dash_shim.js").read_text(encoding="utf-8")
data_tr = load_datasets()
data_en = {k: ({**v, "text": translate_csv(v["text"])} if v["format"] == "csv" else v) for k, v in data_tr.items()}

for lang, page, data in (("tr", page_tr, data_tr), ("en", translate_page(page_tr), data_en)):
    out = D / FILES[lang]
    out.write_text(build(lang, page, data, shim), encoding="utf-8")
    print(f"{out} yazıldı ({out.stat().st_size / 1024:.0f} KB)")
