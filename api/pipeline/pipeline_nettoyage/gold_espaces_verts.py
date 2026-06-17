"""
Gold espaces verts — surface totale et m² par habitant par arrondissement.
Source : OpenData Paris (espaces_verts) + population INSEE (via délinquance Silver)
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SILVER = ROOT / "data" / "Silver"
GOLD = ROOT / "data" / "Gold"

df_ev = pd.read_csv(SILVER / "espaces_verts_clean.csv")
surface = df_ev.groupby("arrondissement")["superficie_m2"].sum().reset_index()
surface.columns = ["arrondissement", "superficie_totale_m2"]

df_pop = pd.read_csv(SILVER / "delinquance_paris.csv", encoding="utf-8-sig")
df_pop["arrondissement"] = df_pop["CODGEO_2025"].astype(str).str[3:5].astype(int)
pop2024 = df_pop[df_pop["annee"] == 2024].groupby("arrondissement")["insee_pop"].first().reset_index()

df = surface.merge(pop2024, on="arrondissement", how="left")
df["m2_par_habitant"] = (df["superficie_totale_m2"] / df["insee_pop"]).round(1)
df["annee"] = 2024

df.to_csv(GOLD / "espaces_verts.csv", index=False)
print(f"✅ Gold espaces verts — {len(df)} lignes")
print(df.sort_values("m2_par_habitant", ascending=False).head(5))