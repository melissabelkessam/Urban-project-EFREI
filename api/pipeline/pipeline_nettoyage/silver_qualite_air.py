import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRONZE = ROOT / "data" / "Bronze"
SILVER = ROOT / "data" / "Silver"

df = pd.read_csv(BRONZE / "qualite_air.csv")

df = df[df["ninsee"].astype(str).str.match(r"^751\d\d$")]
df["arrondissement"] = df["ninsee"].astype(str).str[3:5].astype(int)
df = df[df["arrondissement"].between(1, 20)]

df = df[["arrondissement", "no2", "o3", "pm10"]].copy()
df["annee"] = 2018

df.to_csv(SILVER / "qualite_air_clean.csv", index=False)
print(f"✅ Silver qualité air — {len(df)} lignes")
print(df.head())