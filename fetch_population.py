import json
import urllib.request
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
URL = ("https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
       "?date=1962:2012&format=json&per_page=20000")

# World Bank nüfus verisi (SP.POP.TOTL), göç verisiyle aynı 5 yıllık dönemler
with urllib.request.urlopen(URL, timeout=60) as resp:
    _, rows = json.load(resp)

pop = pd.DataFrame([{"iso3": r["countryiso3code"], "year": int(r["date"]), "population": r["value"]}
                    for r in rows if r["countryiso3code"]])
pop = pop[pop["year"].isin(range(1962, 2013, 5))].dropna()
pop.to_csv(BASE_DIR / "population.csv", index=False)
print(f"{pop['iso3'].nunique()} ülke, {len(pop)} satır kaydedildi")
