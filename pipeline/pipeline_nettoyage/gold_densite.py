import pandas as pd
from pathlib import Path

# --- Définition des chemins absolus ---
ROOT = Path(__file__).resolve().parents[2]   # remonte à "URBAN DATA EFREI"
SILVER = ROOT / "data" / "Silver"
GOLD = ROOT / "data" / "Gold"

# Chargement du fichier Silver
df = pd.read_csv(SILVER / "densite_paris.csv", encoding="utf-8-sig")

# On garde toutes les années + les colonnes utiles
df = df[["arrondissement", "annee", "densite_hab_km2"]]

# Sauvegarde en Gold
GOLD.mkdir(parents=True, exist_ok=True)
df.to_csv(GOLD / "densite.csv", index=False, encoding="utf-8-sig")

print("✅ Gold densité généré avec succès !")
