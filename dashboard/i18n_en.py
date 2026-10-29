"""dashboard_en.html için Türkçe → İngilizce çeviriler (build_standalone.py kullanır).

PAGE: index.html içinde birebir değiştirilen metin parçaları (uzundan kısaya uygulanır).
VALUES: veri dosyalarındaki hücre değerleri (sınıf ve bölge adları); sayfadaki aynı adlar PAGE'de de çevrilir.
"""

VALUES = {
    # Kural tabanlı sınıflar ve k-means kümeleri
    "Sürekli göç alan": "Steady receiver",
    "Sürekli göç veren": "Steady sender",
    "Verenden alana dönen": "Sender → receiver",
    "Alandan verene dönen": "Receiver → sender",
    "Dalgalı": "Fluctuating",
    # Yüzyıl sınıfları
    "Göç alan": "Net receiver",
    "Göç veren": "Net sender",
    "Stabil (±1‰)": "Stable (±1‰)",
    "Nüfus verisi yok": "No population data",
    # Dünya Bankası bölgeleri
    "Doğu Asya ve Pasifik": "East Asia & Pacific",
    "Avrupa ve Orta Asya": "Europe & Central Asia",
    "Latin Amerika ve Karayipler": "Latin America & Caribbean",
    "Orta Doğu ve Kuzey Afrika": "Middle East & North Africa",
    "Kuzey Amerika": "North America",
    "Güney Asya": "South Asia",
    "Sahra Altı Afrika": "Sub-Saharan Africa",
    "Dünya": "World",
}

PAGE = {
    # Sayı biçimi ve sıralama
    "{ decimal: ',', thousands: '.',": "{ decimal: '.', thousands: ',',",
    "'tr-TR'": "'en-US'",
    "' milyon'": "' million'",
    "' bin'": "' thousand'",
    "' Mn'": "' M'",
    "' B'": "' K'",
    "'tr')": "'en')",
    "'‰ / yıl'": "'‰ / yr'",
    "'Dünya'": "'World'",

    # Başlık
    "Dünya Bankası · net göç · 1962–2012 · 5 yıllık dönemler": "World Bank · net migration · 1962–2012 · 5-year periods",
    "Küresel Göç Paneli": "Global Migration Dashboard",
    "1962–2012 toplamında en çok göç alan ülke ": "Over 1962–2012, the largest net receiver was ",
    " kişi), en çok göç veren ": " people) and the largest net sender was ",
    " kişi). ": " people). Of the ",
    " ülkenin ": " countries, ",
    " tanesi dönemlerin neredeyse tamamında göç verdi; yalnızca ": " were net senders in almost every period; only ",
    " ülke sürekli göç aldı.": " were steady receivers.",

    # Sekmeler
    'aria-label="Analizler"': 'aria-label="Analyses"',
    ">Genel bakış<": ">Overview<",
    "Dağılım ve istatistik": "Distribution & statistics",
    "K-means kümeleme": "K-means clustering",
    "Kural tabanlı sınıflar ve k-means kümeleri": "Rule-based classes vs k-means clusters",
    ">Kural tabanlı sınıflar<": ">Rule-based classes<",
    "20. ve 21. yüzyıl": "20th vs 21st century",
    ">Ülke karşılaştırma<": ">Country comparison<",

    # Genel bakış
    "Analizdeki ülke": "Countries analysed",
    " dönem × 5 yıl, bölge toplamları hariç": " periods × 5 years, excluding regional aggregates",
    ">En çok göç alan<": ">Top receiver<",
    ">En çok göç veren<": ">Top sender<",
    " · 1962–2012 toplamı": " · 1962–2012 total",
    "Sınıf: ": "Class: ",
    "Yıllara göre net göç haritası": "Net migration map by period",
    "Her ülkenin seçilen 5 yıllık dönemdeki net göçü. Mavi göç alan, turuncu göç veren ülke. Bir ülkeye tıklayınca Ülke karşılaştırma sekmesinde açılır.":
        "Each country's net migration in the selected 5-year period. Blue = net receiver, orange = net sender. Click a country to open it in the Country comparison tab.",
    "▶ Oynat": "▶ Play",
    "❚❚ Durdur": "❚❚ Pause",
    'aria-label="Dönem"': 'aria-label="Period"',
    "Bölgelere göre net göç": "Net migration by region",
    "Dünya Bankası bölge toplamları, dönem başına kişi. Bir bölgeyi gizlemek için etiketine tıklayın.":
        "World Bank regional aggregates, people per period. Click a label to hide a region.",
    "En çok göç alan ve veren 10 ülke": "Top 10 receiving and sending countries",
    "1962–2012 boyunca 11 dönemin toplam net göçü.": "Total net migration over the 11 periods of 1962–2012.",
    "Her dönemde göç alan ve veren ülke sayısı": "Receiving and sending countries per period",
    "Net göçü sıfırdan büyük ülkeler mavi, küçük ülkeler turuncu.": "Countries with net migration above zero in blue, below zero in orange.",
    "'Sıfır'": "'Zero'",
    ">Sıfır<": ">Zero<",

    # Dağılım
    "Tüm ülke-dönem gözlemleri (ülke × 11 dönem) birlikte. Net göç birkaç büyük ülkede milyonlara çıkarken çoğu ülkede binler düzeyinde kalıyor; dağılım bu yüzden aşırı çarpık ve sivri.":
        "All country-period observations pooled (country × 11 periods). Net migration reaches millions in a few large countries but stays in the thousands for most, so the distribution is extremely skewed and peaked.",
    ">Gözlem<": ">Observations<",
    "Aykırı gözlem (IQR × 1,5)": "Outliers (IQR × 1.5)",
    "Aykırı payı": "Outlier share",
    "Çarpıklık": "Skewness",
    "Basıklık (fazlalık)": "Kurtosis (excess)",
    "Net göç dağılımı": "Distribution of net migration",
    "İşaretli log10 ölçeği: sign(x) · log10(|x| + 1). Sağda göç alan, solda göç veren gözlemler; 6 ≈ bir milyon kişi.":
        "Signed log10 scale: sign(x) · log10(|x| + 1). Receiving observations on the right, sending on the left; 6 ≈ one million people.",
    "Dönemlere göre ülke net göçü": "Country net migration by period",
    "Kutu çeyrekleri, çizgi medyanı gösterir; noktalar o dönemin aykırı ülkeleri. Dikey eksen simetrik logaritmik.":
        "Boxes show quartiles and the line the median; dots are that period's outlier countries. The vertical axis is symmetric log.",
    ">Dönemler arası korelasyon<": ">Correlation between periods<",
    "Ülkelerin bir dönemdeki net göçü ile başka bir dönemdeki net göçü arasındaki Pearson korelasyonu. Komşu dönemler yüksek, uzak dönemler daha düşük ilişkili.":
        "Pearson correlation between countries' net migration in one period and in another. Adjacent periods correlate strongly, distant ones less so.",

    # K-means
    "Her ülkenin 11 dönemlik serisi <b>işaretli log</b> ile dönüştürüldü; böylece hem yön (alan/veren) hem büyüklük korundu ve ABD gibi uç değerler kümeleri domine etmedi.":
        "Each country's 11-period series was transformed with a <b>signed log</b>, keeping both direction (receiving/sending) and magnitude so that extremes like the USA don't dominate the clusters.",
    "K-means, k-means++ başlangıcı ve 20 tekrar ile k = 2…8 için çalıştırıldı.": "K-means was run for k = 2…8 with k-means++ initialisation and 20 restarts.",
    "k = 2 yalnızca alan/veren ayrımı verdiği için en az ": "Since k = 2 only separates receivers from senders, the highest silhouette score among at least ",
    "</b> küme arasından en yüksek silhouette skoru seçildi: <b": "</b> clusters was chosen: <b",
    "</b> küme, skor <b": "</b> clusters, score <b",
    "Kümeler merkez profillerine göre adlandırıldı.": "Clusters were named after their centroid profiles.",
    "Küme sayısına göre silhouette skoru": "Silhouette score by number of clusters",
    "Yüksek skor, ülkelerin kendi kümesine diğer kümelerden daha yakın olduğunu gösterir. Seçilen k koyu işaretli.":
        "A higher score means countries are closer to their own cluster than to the others. The chosen k is highlighted.",
    ">Küme merkez profilleri<": ">Cluster centroid profiles<",
    ">Her kümedeki ülkelerin dönem başına ortalama işaretli log net göçü.<": ">Mean signed-log net migration per period for the countries in each cluster.<",
    "Göç desenine göre ülke kümeleri": "Country clusters by migration pattern",
    "Bir ülkeye tıklayınca Ülke karşılaştırma sekmesinde açılır.": "Click a country to open it in the Country comparison tab.",
    "Her hücre, iki yöntemin aynı ülkeye verdiği etiketlerin kesişimindeki ülke sayısı. K-means 3 kümeyle ters dönüşleri tek grupta toplarken kural tabanlı yöntem yönü ayırıyor.":
        "Each cell counts the countries at the intersection of the two methods' labels. With 3 clusters, k-means lumps reversals into one group while the rule-based method separates their direction.",

    # Kural tabanlı
    '</b>: <b data-draw="sabit" data-key="donem">': '</b>: of the <b data-draw="sabit" data-key="donem">',
    " dönemin en az ": " periods, at least ",
    " tanesinde net göç pozitif.": " have positive net migration.",
    "</b>: en az <b": "</b>: at least <b",
    " dönemde negatif.": " periods with negative net migration.",
    "</b>: ilk 5 dönemin (1962–1982) en az <b": "</b>: a sender in at least <b",
    "</b> tanesinde veren, son 5 dönemin (1992–2012) en az <b": "</b> of the first 5 periods (1962–1982) and a receiver in at least <b",
    "</b> tanesinde alan. 1987 geçiş dönemi.": "</b> of the last 5 (1992–2012). 1987 is the transition period.",
    "</b>: tersi.": "</b>: the reverse.",
    "</b>: hiçbir kurala uymayan ülkeler.": "</b>: countries that match none of the rules.",
    "Kural tabanlı göç sınıfları": "Rule-based migration classes",
    "Ülke listesi": "Country list",
    "Başlığa tıklayarak sıralayın, bir satıra tıklayarak ülkeyi Ülke karşılaştırma sekmesinde açın.":
        "Click a header to sort; click a row to open the country in the Country comparison tab.",
    'placeholder="Ülke veya sınıf ara"': 'placeholder="Search country or class"',
    'aria-label="Ülke ara"': 'aria-label="Search countries"',
    ">Ülke</button>": ">Country</button>",
    "Kural sınıfı": "Rule class",
    "K-means kümesi": "K-means cluster",
    "Toplam net göç": "Total net migration",
    "Pozitif dönem": "Positive periods",
    "20. yy ‰/yıl": "20th c. ‰/yr",
    "21. yy ‰/yıl": "21st c. ‰/yr",

    # Yüzyıllar
    "Nüfusa oranlı karşılaştırma. <b>Yıllık net göç hızı</b>, her 1000 kişi için yılda gelen (+) ya da giden (−) kişi sayısıdır: dönem toplamı ÷ (dönem sayısı × 5) ÷ ortalama nüfus × 1000. Dönem uzunluğundan bağımsız olduğu için 8 dönemlik 20. yüzyıl ile 3 dönemlik 21. yüzyıl karşılaştırılabilir. Eşik <b":
        "Population-adjusted comparison. The <b>annual net migration rate</b> is the number of people arriving (+) or leaving (−) per 1,000 inhabitants per year: period total ÷ (number of periods × 5) ÷ average population × 1000. Because it does not depend on period length, the 8-period 20th century can be compared with the 3-period 21st century. Threshold <b",
    "</b>: üstü göç alan, altı göç veren, arası stabil. Nüfus, Dünya Bankası SP.POP.TOTL serisinden.":
        "</b>: above it is a net receiver, below it a net sender, in between stable. Population from the World Bank SP.POP.TOTL series.",
    "20. yüzyıl (1962–1997)": "20th century (1962–1997)",
    "21. yüzyıl (2002–2012)": "21st century (2002–2012)",
    "</i>Stabil · ": "</i>Stable · ",
    "Sınıf geçişleri": "Class transitions",
    "Satır 20. yüzyıl, sütun 21. yüzyıl sınıfı. Köşegen dışı hücreler rejim değiştiren ülkeler.":
        "Rows are the 20th-century class, columns the 21st-century class. Off-diagonal cells are countries that changed regime.",
    "Oranı en uçta olan ülkeler": "Countries with the most extreme rates",
    "Yıllık net göç hızı (‰), her yüzyılda en yüksek ve en düşük 5 ülke.": "Annual net migration rate (‰): the 5 highest and 5 lowest countries in each century.",
    ">20. yüzyıl<": ">20th century<",
    ">21. yüzyıl<": ">21st century<",

    # Ülke karşılaştırma
    "Ülke profili": "Country profile",
    'aria-label="Ülke"': 'aria-label="Country"',
    "20. yy hız": "20th c. rate",
    "21. yy hız": "21st c. rate",
    "Çubuklar dönem başına net göç; nokta ve çizgi yıllık net göç hızı (‰, sağ eksen).":
        "Bars show net migration per period; the dots and line show the annual net migration rate (‰, right axis).",
    "İkili ısı haritası": "Two-country heatmap",
    "İki ülkenin net göçü (5 yıllık dönem toplamı, B = bin, Mn = milyon kişi) ve yıllık net göç hızı (‰). Hazır çiftler analizde incelediğimiz göç koridorları.":
        "Net migration of two countries (5-year period totals, K = thousand, M = million people) and annual net migration rate (‰). The preset pairs are the migration corridors examined in the analysis.",
    "Türkiye – Almanya": "Türkiye – Germany",
    "ABD – Meksika": "USA – Mexico",
    "Birinci ülke": "First country",
    "İkinci ülke": "Second country",
    "İki ülkenin net göç serisi arasındaki korelasyon (11 dönem)": "Correlation between the two countries' net migration series (11 periods)",
    "Kaynak: Dünya Bankası net göç (SM.POP.NETM, 5 yıllık tahminler, migration.csv) ve toplam nüfus (SP.POP.TOTL). Ülke sınırları Natural Earth tabanlı basitleştirilmiş harita. Analiz kodu:":
        "Source: World Bank net migration (SM.POP.NETM, 5-year estimates, migration.csv) and total population (SP.POP.TOTL). Country borders: simplified map based on Natural Earth. Analysis code:",

    # Grafik ipuçları ve eksenler
    "'Yüklenemedi'": "'Failed to load'",
    "' net göç'": "' net migration'",
    "'Yıllık hız'": "'Annual rate'",
    "'nüfus yok'": "'no population data'",
    "'Gözlem'": "'Observations'",
    "'Medyan'": "'Median'",
    "'Aykırı ülke'": "'Outlier countries'",
    "'Net göç'": "'Net migration'",
    "'Korelasyon'": "'Correlation'",
    "'Atalet'": "'Inertia'",
    "' ülke'": "' countries'",
    "'20. yy', '21. yy'": "'20th c.', '21st c.'",
    "'Nüfus'": "'Population'",
    "'Net göç (kişi, 5 yıllık dönem toplamı · B = bin, Mn = milyon)'": "'Net migration (people, 5-year period total · K = thousand, M = million)'",
    "'Yıllık net göç hızı (‰, nüfusa oranlı)'": "'Annual net migration rate (‰, population-adjusted)'",
}
