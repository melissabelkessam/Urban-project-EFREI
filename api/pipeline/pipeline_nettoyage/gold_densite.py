import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"

def build_densite():
    print("🔄 Construction de l'indicateur : densité de population...")

    df = pd.read_csv(SILVER / "densite_paris.csv")

    # Calculer la densité
    df["densite_hab_km2"] = df["population"] / df["superficie_km2"]

    # Sauvegarde Gold
    output = GOLD / "densite.csv"
    df.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_densite()
