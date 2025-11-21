import pandas as pd
from pathlib import Path

# --- Définition des chemins absolus ---
ROOT = Path(__file__).resolve().parents[2]   # remonte à la racine du projet
SILVER = ROOT / "data" / "Silver"
GOLD = ROOT / "data" / "Gold"

# Charger Silver
df = pd.read_csv(SILVER / "typologie_paris.csv", encoding="utf-8-sig")

# Sauvegarde Gold
GOLD.mkdir(parents=True, exist_ok=True)
df.to_csv(GOLD / "typologie_logements.csv", index=False, encoding="utf-8-sig")

print("✅ Gold typologie généré avec succès !")
