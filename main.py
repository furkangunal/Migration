from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px

from country_codes import to_iso3

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# --- Veriyi yükle ---
df = pd.read_csv(BASE_DIR / "migration.csv")
df = df.rename(columns={"Country Name": "country"})
year_cols = [c for c in df.columns if c != "country"]

# İlk satırlar bölge / gelir grubu toplamları, "World" satırından sonrası ülkeler
world_idx = df.index[df["country"] == "World"][0]
df["is_aggregate"] = df.index <= world_idx
countries = df[~df["is_aggregate"]].copy()
aggregates = df[df["is_aggregate"]].copy()

# --- Genel bakış ---
print("Boyut:", df.shape)
print(f"Ülke: {len(countries)}, Toplam/bölge satırı: {len(aggregates)}")
print("\nVeri tipleri:\n", df.dtypes.value_counts())
print("\nEksik değer sayısı:", df[year_cols].isna().sum().sum())
print("Tekrarlayan ülke adı:", df["country"].duplicated().sum())
print("\nİlk satırlar:\n", df.head())

# --- Tanımlayıcı istatistikler (yalnızca ülkeler) ---
pd.set_option("display.float_format", "{:,.0f}".format)
print("\nYıllara göre tanımlayıcı istatistikler:\n", countries[year_cols].describe().T)

# Uzun formata çevir
long = countries.melt(id_vars="country", value_vars=year_cols,
                      var_name="year", value_name="net_migration")
long["year"] = long["year"].astype(int)
long["iso3"] = to_iso3(long["country"])

# Ülke bazında özet
countries["total"] = countries[year_cols].sum(axis=1)
countries["mean"] = countries[year_cols].mean(axis=1)
countries["std"] = countries[year_cols].std(axis=1)
countries["positive_periods"] = (countries[year_cols] > 0).sum(axis=1)

print("\nToplam net göçte en çok göç ALAN 10 ülke:\n",
      countries.nlargest(10, "total")[["country", "total"]].to_string(index=False))
print("\nToplam net göçte en çok göç VEREN 10 ülke:\n",
      countries.nsmallest(10, "total")[["country", "total"]].to_string(index=False))

# Her dönemde göç alan / veren ülke sayısı
sign_counts = pd.DataFrame({
    "göç alan (>0)": (countries[year_cols] > 0).sum(),
    "göç veren (<0)": (countries[year_cols] < 0).sum(),
    "sıfır": (countries[year_cols] == 0).sum(),
})
print("\nDönemlere göre işaret dağılımı:\n", sign_counts)

# Aykırı değerler (IQR yöntemi, tüm ülke-yıl gözlemleri üzerinde)
q1, q3 = long["net_migration"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = long[(long["net_migration"] < q1 - 1.5 * iqr) | (long["net_migration"] > q3 + 1.5 * iqr)]
print(f"\nAykırı gözlem sayısı (IQR): {len(outliers)} / {len(long)}")

# Çarpıklık / basıklık
print("\nÇarpıklık:", round(long["net_migration"].skew(), 2),
      " Basıklık:", round(long["net_migration"].kurt(), 2))

# Türkiye
tr = countries.loc[countries["country"] == "Turkey", year_cols].iloc[0]
print("\nTürkiye net göç:\n", tr.to_string())

# --- Grafikler ---
figures = {}

# 1) Dünya ve ana bölgeler zaman serisi
regions = ["East Asia & Pacific", "Europe & Central Asia", "Latin America & Caribbean",
           "Middle East & North Africa", "North America", "South Asia", "Sub-Saharan Africa"]
reg_long = aggregates[aggregates["country"].isin(regions)].melt(
    id_vars="country", value_vars=year_cols, var_name="year", value_name="net_migration")
figures["01_bolgeler_zaman_serisi"] = px.line(
    reg_long, x="year", y="net_migration", color="country", markers=True,
    title="Bölgelere göre net göç (5 yıllık)")

# 2) En çok göç alan / veren ülkeler
top_bottom = pd.concat([countries.nlargest(10, "total"), countries.nsmallest(10, "total")])
figures["02_en_cok_alan_veren"] = px.bar(
    top_bottom.sort_values("total"), x="total", y="country", orientation="h",
    color=np.where(top_bottom.sort_values("total")["total"] > 0, "Göç alan", "Göç veren"),
    title="1962–2012 toplam net göç: ilk 10 ve son 10 ülke")

# 3) Dağılım (simetrik log ölçeği ile)
long["signed_log"] = np.sign(long["net_migration"]) * np.log10(np.abs(long["net_migration"]) + 1)
figures["03_dagilim"] = px.histogram(
    long, x="signed_log", nbins=60,
    title="Net göç dağılımı (işaretli log10 ölçeği)")

# 4) Yıllara göre kutu grafiği
figures["04_yillara_gore_kutu"] = px.box(
    long, x="year", y="net_migration", points="outliers",
    title="Yıllara göre ülke net göç dağılımı")

# 5) Isı haritası: mutlak toplamı en yüksek 30 ülke
top30 = countries.loc[countries["total"].abs().nlargest(30).index]
figures["05_isi_haritasi"] = px.imshow(
    top30.set_index("country")[year_cols], aspect="auto",
    color_continuous_scale="RdBu", color_continuous_midpoint=0,
    title="Net göç ısı haritası (mutlak toplamı en yüksek 30 ülke)")

# 6) Dünya haritası (animasyonlu)
figures["06_harita"] = px.choropleth(
    long, locations="iso3", hover_name="country", color="net_migration",
    animation_frame="year", color_continuous_scale="RdBu", range_color=(-2e6, 2e6),
    title="Ülkelere göre net göç")

# 7) Yıllar arası korelasyon
figures["07_yil_korelasyon"] = px.imshow(
    countries[year_cols].corr(), text_auto=".2f", color_continuous_scale="Viridis",
    title="Dönemler arası korelasyon")

# 8) Türkiye
figures["08_turkiye"] = px.bar(
    x=tr.index, y=tr.values, labels={"x": "Yıl", "y": "Net göç"},
    title="Türkiye net göç")

for name, fig in figures.items():
    fig.write_html(OUT_DIR / f"{name}.html")
print(f"\n{len(figures)} grafik kaydedildi: {OUT_DIR}")
