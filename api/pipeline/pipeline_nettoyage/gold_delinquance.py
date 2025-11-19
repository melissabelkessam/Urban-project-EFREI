import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"

def build_delinquance():
    print("🔄 Construction de l'indicateur : délinquance...")

    df = pd.read_csv(SILVER / "delinquance_paris.csv")

    df["arrondissement"] = pd.to_numeric(df["arrondissement"], errors="coerce")
    df["annee"] = pd.to_numeric(df["annee"], errors="coerce")

    df = df.dropna(subset=["arrondissement", "annee"])

    grouped = (
        df.groupby(["arrondissement", "annee"])
        .agg(nb_delits=("nb_delits", "sum"))
        .reset_index()
    )

    output = GOLD / "delinquance.csv"
    grouped.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_delinquance()
