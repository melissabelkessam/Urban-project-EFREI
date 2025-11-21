import pandas as pd
from pathlib import Path

# --- Définition des chemins absolus ---
ROOT = Path(__file__).resolve().parents[2]   # remonte jusqu'au dossier racine du projet
SILVER = ROOT / "data" / "Silver"
GOLD = ROOT / "data" / "Gold"

# Charger Silver
df = pd.read_csv(SILVER / "delinquance_paris.csv", encoding="utf-8-sig")

# Extraire le numéro d'arrondissement 
# CODGEO_2025 contient des codes INSEE comme 75101, 75115, etc.
df["arrondissement"] = df["CODGEO_2025"].astype(str).str[-2:].astype(int)

# Garder seulement les colonnes utiles
df = df[["arrondissement", "annee", "nombre"]]

# Agréger : somme de tous les délits par arrondissement et année
df_agg = df.groupby(["arrondissement", "annee"])["nombre"].sum().reset_index()

# Normalisation par année (score entre 0 et 10)
df_agg["score_delinquance"] = df_agg.groupby("annee")["nombre"].transform(
    lambda x: (x / x.max()) * 10
).round(1)

# Colonnes finales
df_final = df_agg[["arrondissement", "annee", "score_delinquance"]]

# Export vers Gold
GOLD.mkdir(parents=True, exist_ok=True)
df_final.to_csv(GOLD / "delinquance.csv", index=False, encoding="utf-8-sig")

print("✅ Gold délinquance généré avec succès !")
