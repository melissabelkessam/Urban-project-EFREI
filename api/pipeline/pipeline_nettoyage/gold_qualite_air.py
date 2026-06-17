"""
Gold qualité air — moyenne annuelle NO2, O3, PM10 par arrondissement.
Source : Airparif via OpenData Paris (2018)
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SILVER = ROOT / "data" / "Silver"
GOLD = ROOT / "data" / "Gold"

df = pd.read_csv(SILVER / "qualite_air_clean.csv")

gold = df.groupby("arrondissement").agg(
    no2_moyen=("no2", "mean"),
    o3_moyen=("o3", "mean"),
    pm10_moyen=("pm10", "mean")
).reset_index().round(1)

gold["annee"] = 2018

gold.to_csv(GOLD / "qualite_air.csv", index=False)
print(f"✅ Gold qualité air — {len(gold)} lignes")
print(gold.head())