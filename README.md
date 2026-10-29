# Global Migration Dashboard (1962–2012)

[English](#english) · [Türkçe](#türkçe)

**[▶ Open the dashboard / Paneli aç](https://furkangunal.github.io/Migration/dashboard/dashboard.html)**

---

## English

Exploratory analysis of World Bank net migration estimates by country (5-year periods, 1962–2012), two classification approaches (k-means and rule-based), and an interactive dashboard.

### Dashboard

`dashboard/dashboard.html` is a self-contained file: the data is embedded and no server is needed. You can also download the repo and double-click the file. An internet connection is required because the charting library (d3) loads from a CDN. The dashboard text is in Turkish.

| Tab | Contents |
|---|---|
| Genel bakış (Overview) | Animated net migration map by period, regional series, top 10 receiving/sending countries |
| Dağılım ve istatistik (Distribution) | Histogram, box plots by period, correlation between periods, summary statistics |
| K-means kümeleme (Clustering) | Choosing k (silhouette), cluster profiles, cluster map |
| Kural tabanlı sınıflar (Rule-based) | Five migration regimes (steady receiving/sending, reversing, fluctuating), class map, crosstab with k-means |
| 20. ve 21. yüzyıl (20th vs 21st century) | Comparison of annual net migration rates (‰, population-adjusted) |
| Ülke karşılaştırma (Country comparison) | Single-country profile and a two-country heatmap (e.g. Türkiye–Germany, USA–Mexico) |

You can link to a tab directly, for example `dashboard.html#ulkeler`.

### Data

- `migration.csv`: World Bank net migration, [SM.POP.NETM](https://data.worldbank.org/indicator/SM.POP.NETM) (5-year period totals)
- `population.csv`: World Bank total population, [SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL) (downloaded by `fetch_population.py`)
- `dashboard/geo_dl/countries.geo.json`: country borders based on Natural Earth

### Project structure

```
├── migration.csv, population.csv   raw data
├── country_codes.py                country name → ISO3 mapping
├── fetch_population.py             downloads population data from the World Bank API
├── main.py                         exploratory analysis charts
├── clustering.py                   k-means clustering (signed-log series)
├── rule_based.py                   rule-based migration regime classification
├── turkiye_almanya.py              two-country heatmaps
├── outputs/                        class CSVs (+ Plotly HTML charts, not in the repo)
└── dashboard/
    ├── prep.py                     builds the dashboard datasets → dashboard/data/
    ├── index.html                  dashboard page (claude.ai Dashboard format)
    ├── dash_shim.js                standalone stand-in for the runtime the page expects
    ├── build_standalone.py         index.html + data/ → single-file dashboard.html
    └── dashboard.html              the published standalone dashboard
```

### Reproducing

```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python fetch_population.py        # optional: population.csv is already in the repo
python main.py
python clustering.py              # → outputs/ulke_kumeleri.csv
python rule_based.py              # → outputs/ulke_kural_siniflari.csv
python turkiye_almanya.py
python dashboard/prep.py          # → dashboard/data/
python dashboard/build_standalone.py   # → dashboard/dashboard.html
```

The analysis scripts write detailed Plotly charts to `outputs/` as HTML files.

---

## Türkçe

Dünya Bankası'nın ülke bazında net göç tahminleri (5 yıllık dönemler, 1962–2012) üzerine keşifsel analiz. Proje iki sınıflandırma yöntemi (k-means ve kural tabanlı) ve etkileşimli bir dashboard içeriyor.

### Dashboard

`dashboard/dashboard.html` tek başına çalışan bir dosyadır. Veriler içine gömülüdür, sunucu gerekmez. Repoyu indirip dosyaya çift tıklamak da yeterlidir. Grafik kütüphanesi d3 CDN'den yüklendiği için internet bağlantısı gerekir.

| Sekme | İçerik |
|---|---|
| Genel bakış | Yıllara göre net göç haritası (oynatılabilir), bölge serileri, en çok göç alan/veren 10 ülke |
| Dağılım ve istatistik | Histogram, dönemlere göre kutu grafiği, dönemler arası korelasyon, temel istatistikler |
| K-means kümeleme | Küme sayısı seçimi (silhouette), küme profilleri, küme haritası |
| Kural tabanlı sınıflar | Beş göç rejimi (sürekli alan/veren, dönen, dalgalı), sınıf haritası, k-means ile çapraz tablo |
| 20. ve 21. yüzyıl | Nüfusa oranlı yıllık net göç hızı (‰) ile iki dönemin karşılaştırması |
| Ülke karşılaştırma | Tek ülke profili ve iki ülkenin dönem dönem ısı haritası (ör. Türkiye–Almanya, ABD–Meksika) |

Bir sekmeye doğrudan bağlantı verilebilir, örneğin `dashboard.html#ulkeler`.

### Veri

- `migration.csv`: Dünya Bankası net göç, [SM.POP.NETM](https://data.worldbank.org/indicator/SM.POP.NETM) (5 yıllık dönem toplamları)
- `population.csv`: Dünya Bankası toplam nüfus, [SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL) (`fetch_population.py` ile indirilir)
- `dashboard/geo_dl/countries.geo.json`: Natural Earth tabanlı ülke sınırları

### Proje yapısı

```
├── migration.csv, population.csv   ham veri
├── country_codes.py                ülke adı → ISO3 eşlemesi
├── fetch_population.py             nüfus verisini Dünya Bankası API'sinden indirir
├── main.py                         keşifsel analiz grafikleri
├── clustering.py                   k-means kümeleme (işaretli log seriler)
├── rule_based.py                   kural tabanlı göç rejimi sınıflandırması
├── turkiye_almanya.py              ikili ülke ısı haritaları
├── outputs/                        sınıf CSV'leri (+ Plotly HTML grafikleri, repoda yok)
└── dashboard/
    ├── prep.py                     dashboard veri setlerini üretir → dashboard/data/
    ├── index.html                  dashboard sayfası (claude.ai Dashboard biçiminde)
    ├── dash_shim.js                sayfanın beklediği çalışma ortamının bağımsız karşılığı
    ├── build_standalone.py         index.html + data/ → tek dosyalık dashboard.html
    └── dashboard.html              yayınlanan, tek başına çalışan panel
```

### Yeniden üretmek

```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python fetch_population.py        # isteğe bağlı: population.csv zaten repoda
python main.py
python clustering.py              # → outputs/ulke_kumeleri.csv
python rule_based.py              # → outputs/ulke_kural_siniflari.csv
python turkiye_almanya.py
python dashboard/prep.py          # → dashboard/data/
python dashboard/build_standalone.py   # → dashboard/dashboard.html
```

Analiz betikleri ayrıntılı Plotly grafiklerini `outputs/` klasörüne HTML olarak yazar.
