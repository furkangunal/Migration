    from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px

from country_codes import to_iso3

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)
RNG = np.random.default_rng(42)

# --- Veriyi yükle, yalnızca ülkeleri al ---
df = pd.read_csv(BASE_DIR / "migration.csv").rename(columns={"Country Name": "country"})
year_cols = [c for c in df.columns if c != "country"]
world_idx = df.index[df["country"] == "World"][0]
countries = df.loc[world_idx + 1:].reset_index(drop=True)
countries["iso3"] = to_iso3(countries["country"])

# İşaretli log dönüşümü: hem yönü (alan/veren) hem büyüklüğü korur,
# ABD gibi uç değerlerin kümeleri domine etmesini engeller
X = np.sign(countries[year_cols].to_numpy()) * np.log10(np.abs(countries[year_cols].to_numpy()) + 1)


def kmeans(X, k, n_init=20, max_iter=300):
    best_labels, best_centers, best_inertia = None, None, np.inf
    for _ in range(n_init):
        # k-means++ başlangıcı
        centers = [X[RNG.integers(len(X))]]
        for _ in range(k - 1):
            d2 = np.min(((X[:, None] - np.array(centers)) ** 2).sum(-1), axis=1)
            centers.append(X[RNG.choice(len(X), p=d2 / d2.sum())])
        centers = np.array(centers)
        for _ in range(max_iter):
            labels = ((X[:, None] - centers) ** 2).sum(-1).argmin(1)
            new = np.array([X[labels == j].mean(0) if np.any(labels == j) else centers[j] for j in range(k)])
            if np.allclose(new, centers):
                break
            centers = new
        inertia = ((X - centers[labels]) ** 2).sum()
        if inertia < best_inertia:
            best_labels, best_centers, best_inertia = labels, centers, inertia
    return best_labels, best_centers, best_inertia


def silhouette(X, labels):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    s = np.zeros(len(X))
    for i in range(len(X)):
        same = labels == labels[i]
        if same.sum() == 1:
            continue
        a = D[i, same].sum() / (same.sum() - 1)
        b = min(D[i, labels == j].mean() for j in np.unique(labels) if j != labels[i])
        s[i] = (b - a) / max(a, b)
    return s.mean()


# --- Küme sayısını seç ---
scores = []
for k in range(2, 9):
    labels, _, inertia = kmeans(X, k)
    scores.append({"k": k, "inertia": inertia, "silhouette": silhouette(X, labels)})
scores = pd.DataFrame(scores)
print("Küme sayısı seçimi:\n", scores.round(3).to_string(index=False))

# k=2 genelde sadece alan/veren ayrımı verir; desen için en az 3 küme ara
best_k = int(scores.loc[scores["k"] >= 3].sort_values("silhouette", ascending=False).iloc[0]["k"])
labels, centers, _ = kmeans(X, best_k)
print(f"\nSeçilen küme sayısı: {best_k}")

# --- Kümeleri merkez profillerine göre adlandır ---
early, late = centers[:, :5].mean(1), centers[:, -5:].mean(1)


def describe(c, e, l):
    pos = (c > 0).sum()
    if pos >= 9:
        return "Sürekli göç alan"
    if pos <= 2:
        return "Sürekli göç veren"
    if e < 0 < l:
        return "Verenden alana dönen"
    if e > 0 > l:
        return "Alandan verene dönen"
    return "Dalgalı / dengeye yakın"


names = [describe(c, e, l) for c, e, l in zip(centers, early, late)]
# Aynı adı alan kümeleri büyüklüğe göre ayırt et
order = np.argsort(-np.abs(centers).mean(1))
seen = {}
for j in order:
    seen[names[j]] = seen.get(names[j], 0) + 1
    if seen[names[j]] > 1 or names.count(names[j]) > 1:
        names[j] += " (güçlü)" if seen[names[j]] == 1 else " (zayıf)"

countries["cluster"] = [names[l] for l in labels]
countries["total"] = countries[year_cols].sum(axis=1)

# --- Özet ---
for j in np.argsort(-centers.mean(1)):
    members = countries[labels == j].sort_values("total", key=abs, ascending=False)
    print(f"\n=== {names[j]} — {len(members)} ülke ===")
    print("Medyan net göç:", members[year_cols].median().astype(int).to_dict())
    print("Örnekler:", ", ".join(members["country"].head(15)))
bu
countries[["country", "cluster", "total", *year_cols]].to_csv(OUT_DIR / "ulke_kumeleri.csv", index=False)

# --- Grafikler ---
long = countries.melt(id_vars=["country", "cluster"], value_vars=year_cols,
                      var_name="year", value_name="net_migration")
long["signed_log"] = np.sign(long["net_migration"]) * np.log10(np.abs(long["net_migration"]) + 1)

profile = pd.DataFrame(centers, columns=year_cols).assign(cluster=names).melt(
    id_vars="cluster", var_name="year", value_name="signed_log")
px.line(profile, x="year", y="signed_log", color="cluster", markers=True,
        title="Küme merkez profilleri (işaretli log10 net göç)").write_html(OUT_DIR / "09_kume_profilleri.html")

px.line(long, x="year", y="signed_log", color="cluster", line_group="country",
        facet_col="cluster", facet_col_wrap=3, hover_name="country",
        title="Kümelere göre ülke serileri").update_traces(opacity=0.4) \
    .write_html(OUT_DIR / "10_kume_ulke_serileri.html")

px.choropleth(countries, locations="iso3", hover_name="country", color="cluster",
              hover_data={"total": ":,"}, title="Göç desenine göre ülke kümeleri") \
    .write_html(OUT_DIR / "11_kume_haritasi.html")

px.line(scores, x="k", y="silhouette", markers=True,
        title="Küme sayısına göre silhouette skoru").write_html(OUT_DIR / "12_silhouette.html")

print(f"\nKüme listesi ve 4 grafik kaydedildi: {OUT_DIR}")
