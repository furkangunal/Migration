# Global Migration Dashboard (1962–2012)

[English](#english) · [Türkçe](#türkçe)

**[▶ Open the dashboard (English)](https://furkangunal.github.io/Migration/dashboard/dashboard_en.html)** · **[▶ Paneli aç (Türkçe)](https://furkangunal.github.io/Migration/dashboard/dashboard.html)**

**Presentations / Sunumlar:** [Migration and History 1962–2012 (EN, PDF)](presentations/Migration%20and%20History%201962%E2%80%932012.pdf) · [Göç ve Tarih 1962–2012 (TR, PDF)](presentations/G%C3%B6%C3%A7%20ve%20Tarih%201962%E2%80%932012.pdf)

---

## English

Exploratory analysis of World Bank net migration estimates by country (5-year periods, 1962–2012), two classification approaches (k-means and rule-based), and an interactive dashboard.

### Dashboard

The dashboard comes in two languages: `dashboard/dashboard_en.html` (English) and `dashboard/dashboard.html` (Turkish). Use the **TR | EN** switch in the header to change language; the open tab is kept. Both are self-contained files: the data is embedded and no server is needed. You can also download the repo and double-click a file. An internet connection is required because the charting library (d3) loads from a CDN.

| Tab | Contents |
|---|---|
| Overview | Animated net migration map by period, regional series, top 10 receiving/sending countries |
| Distribution & statistics | Histogram, box plots by period, correlation between periods, summary statistics |
| K-means clustering | Choosing k (silhouette), cluster profiles, cluster map |
| Rule-based classes | Five migration regimes (steady receiver/sender, reversing, fluctuating), class map, crosstab with k-means |
| 20th vs 21st century | Comparison of annual net migration rates (‰, population-adjusted) |
| Country comparison | Single-country profile and a two-country heatmap (e.g. Türkiye–Germany, USA–Mexico) |

You can link to a tab directly, for example `dashboard_en.html#ulkeler`.

### Presentations

The `presentations/` folder holds the slide decks for this project as PDFs: *Migration and History 1962–2012* (English) and *Göç ve Tarih 1962–2012* (Turkish).

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
├── presentations/                  slide decks (PDF, English and Turkish)
└── dashboard/
    ├── prep.py                     builds the dashboard datasets → dashboard/data/
    ├── index.html                  dashboard page (claude.ai Dashboard format)
    ├── dash_shim.js                standalone stand-in for the runtime the page expects
    ├── i18n_en.py                  Turkish → English translations
    ├── build_standalone.py         index.html + data/ → dashboard.html (TR) and dashboard_en.html (EN)
    ├── dashboard.html              standalone dashboard, Turkish
    └── dashboard_en.html           standalone dashboard, English
```

## Türkçe

Dünya Bankası'nın ülke bazında net göç tahminleri (5 yıllık dönemler, 1962–2012) üzerine keşifsel analiz. Proje iki sınıflandırma yöntemi (k-means ve kural tabanlı) ve etkileşimli bir dashboard içeriyor.

### Dashboard

Panel iki dilde: `dashboard/dashboard.html` (Türkçe) ve `dashboard/dashboard_en.html` (İngilizce). Başlıktaki **TR | EN** düğmesiyle dil değiştirilir, açık sekme korunur. İkisi de tek başına çalışan dosyalardır. Veriler içine gömülüdür, sunucu gerekmez. Repoyu indirip dosyaya çift tıklamak da yeterlidir. Grafik kütüphanesi d3 CDN'den yüklendiği için internet bağlantısı gerekir.

| Sekme | İçerik |
|---|---|
| Genel bakış | Yıllara göre net göç haritası (oynatılabilir), bölge serileri, en çok göç alan/veren 10 ülke |
| Dağılım ve istatistik | Histogram, dönemlere göre kutu grafiği, dönemler arası korelasyon, temel istatistikler |
| K-means kümeleme | Küme sayısı seçimi (silhouette), küme profilleri, küme haritası |
| Kural tabanlı sınıflar | Beş göç rejimi (sürekli alan/veren, dönen, dalgalı), sınıf haritası, k-means ile çapraz tablo |
| 20. ve 21. yüzyıl | Nüfusa oranlı yıllık net göç hızı (‰) ile iki dönemin karşılaştırması |
| Ülke karşılaştırma | Tek ülke profili ve iki ülkenin dönem dönem ısı haritası (ör. Türkiye–Almanya, ABD–Meksika) |

Bir sekmeye doğrudan bağlantı verilebilir, örneğin `dashboard.html#ulkeler`.

### Sunumlar

`presentations/` klasöründe projenin sunumları PDF olarak bulunur: *Göç ve Tarih 1962–2012* (Türkçe) ve *Migration and History 1962–2012* (İngilizce).

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
├── presentations/                  sunumlar (PDF, Türkçe ve İngilizce)
└── dashboard/
    ├── prep.py                     dashboard veri setlerini üretir → dashboard/data/
    ├── index.html                  dashboard sayfası (claude.ai Dashboard biçiminde)
    ├── dash_shim.js                sayfanın beklediği çalışma ortamının bağımsız karşılığı
    ├── i18n_en.py                  Türkçe → İngilizce çeviriler
    ├── build_standalone.py         index.html + data/ → dashboard.html (TR) ve dashboard_en.html (EN)
    ├── dashboard.html              tek başına çalışan panel, Türkçe
    └── dashboard_en.html           tek başına çalışan panel, İngilizce
```
