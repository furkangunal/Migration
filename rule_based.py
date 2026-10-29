from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from country_codes import to_iso3

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# Eşikler
STEADY_MIN = 9      # 11 dönemin en az bu kadarında aynı yön -> "sürekli"
HALF_MAJORITY = 3   # 5 dönemlik yarıda en az bu kadar aynı yön -> o yarının yönü

# --- Veriyi yükle, yalnızca ülkeleri al ---
df = pd.read_csv(BASE_DIR / "migration.csv").rename(columns={"Country Name": "country"})
year_cols = [c for c in df.columns if c != "country"]
world_idx = df.index[df["country"] == "World"][0]
countries = df.loc[world_idx + 1:].reset_index(drop=True)
countries["iso3"] = to_iso3(countries["country"])

values = countries[year_cols]
early, late = year_cols[:5], year_cols[-5:]   # 1962–1982 ve 1992–2012 (1987 geçiş dönemi)

countries["pos_periods"] = (values > 0).sum(axis=1)
countries["neg_periods"] = (values < 0).sum(axis=1)
countries["early_pos"] = (values[early] > 0).sum(axis=1)
countries["early_neg"] = (values[early] < 0).sum(axis=1)
countries["late_pos"] = (values[late] > 0).sum(axis=1)
countries["late_neg"] = (values[late] < 0).sum(axis=1)


def classify(r):
    if r["pos_periods"] >= STEADY_MIN:
        return "Sürekli göç alan"
    if r["neg_periods"] >= STEADY_MIN:
        return "Sürekli göç veren"
    if r["early_neg"] >= HALF_MAJORITY and r["late_pos"] >= HALF_MAJORITY:
        return "Verenden alana dönen"
    if r["early_pos"] >= HALF_MAJORITY and r["late_neg"] >= HALF_MAJORITY:
        return "Alandan verene dönen"
    return "Dalgalı"


countries["rule_class"] = countries.apply(classify, axis=1)
countries["total"] = values.sum(axis=1)

# --- Özet ---
print("Sınıf büyüklükleri:\n", countries["rule_class"].value_counts().to_string())
for cls, members in countries.groupby("rule_class"):
    members = members.sort_values("total", key=abs, ascending=False)
    print(f"\n=== {cls} — {len(members)} ülke ===")
    print(", ".join(members["country"]))

# K-means sonucuyla karşılaştır
kmeans_path = OUT_DIR / "ulke_kumeleri.csv"
if kmeans_path.exists():
    km = pd.read_csv(kmeans_path)[["country", "cluster"]]
    merged = countries.merge(km, on="country")
    print("\nKural tabanlı (satır) vs k-means (sütun):\n",
          pd.crosstab(merged["rule_class"], merged["cluster"]).to_string())

countries[["country", "rule_class", "total", "pos_periods", "neg_periods", *year_cols]] \
    .to_csv(OUT_DIR / "ulke_kural_siniflari.csv", index=False)

# --- Grafikler ---
long = countries.melt(id_vars=["country", "rule_class"], value_vars=year_cols,
                      var_name="year", value_name="net_migration")
px.line(long, x="year", y="net_migration", color="rule_class", line_group="country",
        facet_col="rule_class", facet_col_wrap=3, hover_name="country",
        title="Kural tabanlı sınıflara göre ülke serileri") \
    .update_yaxes(matches=None).update_traces(opacity=0.5) \
    .write_html(OUT_DIR / "13_kural_ulke_serileri.html")

px.choropleth(countries, locations="iso3", hover_name="country", color="rule_class",
              hover_data={"total": ":,", "pos_periods": True},
              title="Kural tabanlı göç sınıfları") \
    .write_html(OUT_DIR / "14_kural_haritasi.html")

print(f"\nSınıf listesi ve 2 grafik kaydedildi: {OUT_DIR}")




# --- Yüzyıllara göre nüfusa oranlı sınıflama ---
# Yıllık net göç hızı (‰): her 1000 kişi için yılda gelen (+) / giden (-) kişi.
# Dönem sayısından bağımsız, böylece 8 dönemlik 20. yy ile 3 dönemlik 21. yy karşılaştırılabilir.
# > +1‰ -> göç alan, < -1‰ -> göç veren, arası -> stabil
THRESHOLD = 1.0  # ‰ / yıl
pop = pd.read_csv(BASE_DIR / "population.csv")  # fetch_population.py ile indirilir
pop_wide = pop.pivot(index="iso3", columns="year", values="population")
pop_wide.columns = pop_wide.columns.astype(str)

centuries = {
    "20. yüzyıl (1962–1997)": [c for c in year_cols if int(c) < 2000],
    "21. yüzyıl (2002–2012)": [c for c in year_cols if int(c) >= 2000],
}
class_colors = {"Göç alan": "#2166ac", "Stabil (±1‰)": "#bdbdbd", "Göç veren": "#b2182b"}

century_frames = []
for label, cols in centuries.items():
    frame = countries[["country", "iso3"]].copy()
    frame["century"] = label
    frame["net"] = countries[cols].sum(axis=1)
    frame["avg_pop"] = pop_wide.reindex(countries["iso3"])[cols].mean(axis=1).to_numpy()
    frame["rate"] = frame["net"] / (len(cols) * 5) / frame["avg_pop"] * 1000
    frame["class"] = np.select(
        [frame["rate"].isna(), frame["rate"] > THRESHOLD, frame["rate"] < -THRESHOLD],
        ["Nüfus verisi yok", "Göç alan", "Göç veren"], default="Stabil (±1‰)")
    century_frames.append(frame)
by_century = pd.concat(century_frames, ignore_index=True)

print("\nYüzyıllara göre sınıf büyüklükleri (yıllık ‰ net göç hızı):\n",
      pd.crosstab(by_century["class"], by_century["century"]).to_string())
wide = by_century.pivot(index="country", columns="century", values="class")
print("\nSınıf geçişleri (20. yy satır, 21. yy sütun):\n",
      pd.crosstab(wide.iloc[:, 0], wide.iloc[:, 1]).to_string())
for label, frame in by_century.groupby("century"):
    print(f"\n{label} — oranı en yüksek / en düşük 5 ülke:")
    ranked = frame.dropna(subset=["rate"]).sort_values("rate")
    print("  Alan:", ", ".join(f"{r.country} ({r.rate:+.1f}‰)" for r in ranked.tail(5)[::-1].itertuples()))
    print("  Veren:", ", ".join(f"{r.country} ({r.rate:+.1f}‰)" for r in ranked.head(5).itertuples()))
tr = by_century[by_century["country"] == "Turkey"]
print("\nTürkiye:", {r.century: f"{r['class']} ({r.rate:+.2f}‰)" for _, r in tr.iterrows()})

# İki harita yan yana, her birinin sınıf açıklaması kendi altında
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "geo"}, {"type": "geo"}]],
                    subplot_titles=list(centuries), horizontal_spacing=0.02)
for i, label in enumerate(centuries, start=1):
    frame = by_century[by_century["century"] == label]
    legend = "legend" if i == 1 else "legend2"
    for cls, color in class_colors.items():
        part = frame[frame["class"] == cls]
        fig.add_trace(go.Choropleth(
            locations=part["iso3"], z=np.ones(len(part)), name=cls,
            colorscale=[[0, color], [1, color]], showscale=False, showlegend=True, legend=legend,
            text=part["country"], customdata=part[["rate", "net"]],
            hovertemplate="<b>%{text}</b><br>Yıllık net göç hızı: %{customdata[0]:+.2f}‰"
                          "<br>Toplam net göç: %{customdata[1]:,}<extra>" + cls + "</extra>",
        ), row=1, col=i)

legend_style = dict(orientation="h", yanchor="top", y=0.02, xanchor="center", title_text="")
fig.update_layout(
    title="Nüfusa oranla net göç: 20. yüzyıl ve 21. yüzyıl (eşik ±1‰ / yıl)",
    height=600, margin=dict(l=10, r=10, t=80, b=40),
    legend=dict(**legend_style, x=0.25), legend2=dict(**legend_style, x=0.75),
)
fig.update_geos(showframe=False, projection_type="natural earth")
fig.write_html(OUT_DIR / "15_kural_haritasi_yuzyillar.html")
print(f"\nYüzyıl haritası kaydedildi: {OUT_DIR / '15_kural_haritasi_yuzyillar.html'}")
