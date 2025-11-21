import pandas as pd
from pathlib import Path

# Définir le chemin vers le dossier Silver
ROOT = Path(__file__).resolve().parents[2]
SILVER = ROOT / "data" / "Silver"

# Fichier densité
fichier = SILVER / "densite_paris.csv"

# Lecture du CSV
df = pd.read_csv(fichier, sep=",", encoding="utf-8-sig")

# Récupération des années min/max
annee_min = int(df["annee"].min())
annee_max = int(df["annee"].max())

# Affichage
print("Première année :", annee_min)
print("Dernière année :", annee_max)
