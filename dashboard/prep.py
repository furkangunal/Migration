import json, math, sys
from pathlib import Path
import numpy as np, pandas as pd
BASE = Path(r"C:/Users/ASUS/Desktop/DATA/Migration"); sys.path.insert(0, str(BASE))
from country_codes import to_iso3
S = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent; OUT = S / "data"; OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "migration.csv").rename(columns={"Country Name": "country"})
year_cols = [c for c in df.columns if c != "country"]
world_idx = df.index[df["country"] == "World"][0]
regions = {"East Asia & Pacific": "Doğu Asya ve Pasifik", "Europe & Central Asia": "Avrupa ve Orta Asya",
           "Latin America & Caribbean": "Latin Amerika ve Karayipler", "Middle East & North Africa": "Orta Doğu ve Kuzey Afrika",
           "North America": "Kuzey Amerika", "South Asia": "Güney Asya", "Sub-Saharan Africa": "Sahra Altı Afrika"}
countries = df.loc[world_idx + 1:].reset_index(drop=True)
countries["iso3"] = to_iso3(countries["country"])
pop = pd.read_csv(BASE / "population.csv")
popw = pop.pivot(index="iso3", columns="year", values="population"); popw.columns = popw.columns.astype(str)

# seriler (uzun)
rows = []
for _, r in countries.iterrows():
    for y in year_cols:
        p = popw.loc[r.iso3, y] if r.iso3 in popw.index else np.nan
        v = r[y]
        rows.append({"country": r.country, "iso3": r.iso3, "year": int(y), "net": int(v),
                     "population": None if pd.isna(p) else int(p),
                     "rate": None if pd.isna(p) else round(v / 5 / p * 1000, 3),
                     "signed_log": round(float(np.sign(v) * np.log10(abs(v) + 1)), 4)})
pd.DataFrame(rows).to_csv(OUT / "ulke_serileri.csv", index=False)

reg = df[df["country"].isin(list(regions) + ["World"])]
rr = [{"region": regions.get(r.country, "Dünya"), "year": int(y), "net": int(r[y])} for _, r in reg.iterrows() for y in year_cols]
pd.DataFrame(rr).to_csv(OUT / "bolge_serileri.csv", index=False)

# ulkeler
km = pd.read_csv(BASE / "outputs/ulke_kumeleri.csv")[["country", "cluster"]]
rb = pd.read_csv(BASE / "outputs/ulke_kural_siniflari.csv")[["country", "rule_class", "pos_periods", "neg_periods"]]
u = countries[["country", "iso3"]].copy()
u["total"] = countries[year_cols].sum(axis=1).astype(int)
u = u.merge(km, on="country").merge(rb, on="country")
for key, cols in {"20": [c for c in year_cols if int(c) < 2000], "21": [c for c in year_cols if int(c) >= 2000]}.items():
    net = countries[cols].sum(axis=1)
    ap = popw.reindex(countries["iso3"])[cols].mean(axis=1).to_numpy()
    rate = net / (len(cols) * 5) / ap * 1000
    u[f"rate_{key}"] = rate.round(3)
    u[f"class_{key}"] = np.select([rate.isna(), rate > 1, rate < -1], ["Nüfus verisi yok", "Göç alan", "Göç veren"], default="Stabil (±1‰)")
u.to_csv(OUT / "ulkeler.csv", index=False)
print(u["cluster"].value_counts(), u["rule_class"].value_counts())

# k seçimi (clustering.py ile aynı RNG sırası)
RNG = np.random.default_rng(42)
X = np.sign(countries[year_cols].to_numpy()) * np.log10(np.abs(countries[year_cols].to_numpy()) + 1)
def kmeans(X, k, n_init=20, max_iter=300):
    best = (None, None, np.inf)
    for _ in range(n_init):
        centers = [X[RNG.integers(len(X))]]
        for _ in range(k - 1):
            d2 = np.min(((X[:, None] - np.array(centers)) ** 2).sum(-1), axis=1)
            centers.append(X[RNG.choice(len(X), p=d2 / d2.sum())])
        centers = np.array(centers)
        for _ in range(max_iter):
            labels = ((X[:, None] - centers) ** 2).sum(-1).argmin(1)
            new = np.array([X[labels == j].mean(0) if np.any(labels == j) else centers[j] for j in range(k)])
            if np.allclose(new, centers): break
            centers = new
        inertia = ((X - centers[labels]) ** 2).sum()
        if inertia < best[2]: best = (labels, centers, inertia)
    return best
def silhouette(X, labels):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); s = np.zeros(len(X))
    for i in range(len(X)):
        same = labels == labels[i]
        if same.sum() == 1: continue
        a = D[i, same].sum() / (same.sum() - 1)
        b = min(D[i, labels == j].mean() for j in np.unique(labels) if j != labels[i])
        s[i] = (b - a) / max(a, b)
    return s.mean()
sc = []
for k in range(2, 9):
    l, _, ine = kmeans(X, k); sc.append({"k": k, "inertia": round(ine, 2), "silhouette": round(silhouette(X, l), 4)})
pd.DataFrame(sc).to_csv(OUT / "kume_secimi.csv", index=False); print(pd.DataFrame(sc))

# harita: Natural Earth projeksiyonu, önceden hesaplanmış SVG yolları
geo = json.load(open(S / "geo_dl/countries.geo.json", encoding="utf-8"))
def proj(lon, lat):
    l, p = math.radians(lon), math.radians(lat); p2 = p * p; p4 = p2 * p2
    x = l * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = p * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x, y
W = 1000; sx = W / (2 * proj(180, 0)[0]); top = proj(0, 84)[1]
def pt(c):
    x, y = proj(*c[:2]); return f"{(x * sx + W / 2):.1f},{((top - y) * sx):.1f}"
feats = []
for f in geo["features"]:
    if f["id"] == "ATA": continue
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    d = "".join("M" + "L".join(pt(c) for c in ring) + "Z" for poly in polys for ring in poly)
    feats.append({"iso3": f["id"], "name": f["properties"]["name"], "d": d})
print("height", round((top - proj(0, -58)[1]) * sx, 1))
json.dump(feats, open(OUT / "dunya_haritasi.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
