from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from country_codes import to_iso3

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(BASE_DIR / "migration.csv").rename(columns={"Country Name": "country"})
year_cols = [c for c in df.columns if c != "country"]
pop = pd.read_csv(BASE_DIR / "population.csv").pivot(index="iso3", columns="year", values="population")
pop.columns = pop.columns.astype(str)

# Sütun etiketleri: verideki yıl ve kapsadığı 5 yıllık dönem
periods = [f"{int(y) - 2}–{str(int(y) + 3)[-2:]}" for y in year_cols]


def pair_heatmap(labels: dict[str, str], out_name: str):
    """labels: {veri setindeki ad: grafikte görünen ad}"""
    pair = df.set_index("country").loc[list(labels), year_cols]

    # Yıllık net göç hızı (‰): 5 yıllık toplam / 5 / nüfus * 1000
    pair_pop = pop.loc[to_iso3(pd.Series(pair.index)).tolist(), year_cols].set_axis(pair.index)
    rate = pair / 5 / pair_pop * 1000
    rows = list(labels.values())

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.18,
                        subplot_titles=["Net göç (bin kişi, 5 yıllık dönem toplamı)",
                                        "Yıllık net göç hızı (‰, nüfusa oranlı)"])
    for i, (values, fmt, unit) in enumerate([(pair / 1000, "{:+,.0f}", "bin kişi"), (rate, "{:+.1f}", "‰")], start=1):
        limit = np.abs(values.to_numpy()).max()
        fig.add_trace(go.Heatmap(
            z=values.to_numpy(), x=periods, y=rows,
            text=[[fmt.format(v) for v in row] for row in values.to_numpy()], texttemplate="%{text}",
            colorscale="RdBu", zmin=-limit, zmax=limit, zmid=0,
            colorbar=dict(title=unit, len=0.4, y=0.8 if i == 1 else 0.2),
            hovertemplate="%{y} · %{x}<br>%{text} " + unit + "<extra></extra>",
        ), row=i, col=1)

    corr = pair.T.corr().iloc[0, 1]
    fig.update_layout(
        title=f"{' ve '.join(rows)} net göç ısı haritası (iki ülke arasındaki korelasyon: {corr:+.2f})",
        height=520,
    )
    fig.update_yaxes(autorange="reversed")
    fig.write_html(OUT_DIR / out_name)

    print(f"=== {' – '.join(rows)} ===")
    print("Net göç (bin kişi):\n", (pair / 1000).round(0).astype(int).set_axis(periods, axis=1).to_string())
    print("\nYıllık net göç hızı (‰):\n", rate.round(2).set_axis(periods, axis=1).to_string())
    print(f"\nKorelasyon (net göç, 11 dönem): {corr:+.2f}\n")


pair_heatmap({"Turkey": "Türkiye", "Germany": "Almanya"}, "16_turkiye_almanya_isi_haritasi.html")
pair_heatmap({"United States": "ABD", "Mexico": "Meksika"}, "17_abd_meksika_isi_haritasi.html")
