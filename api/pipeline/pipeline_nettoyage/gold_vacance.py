import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"

def build_vacance():
    print("🔄 Construction de l'indicateur : vacance des logements...")

    df = pd.read_csv(SILVER / "vacance_paris.csv")

    # Rien à calculer, les valeurs sont déjà prêtes
    output = GOLD / "vacance.csv"
    df.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_vacance()
