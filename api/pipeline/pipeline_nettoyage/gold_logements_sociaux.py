import pandas as pd
from pathlib import Path

# Chemins adaptés à ta structure
ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"

def build_logements_sociaux():
    print("🔄 Construction de l'indicateur : logements sociaux (programmes)…")

    # Charger fichier Silver
    df = pd.read_csv(SILVER / "logements_sociaux_clean.csv")

    # Vérifier colonnes nécessaires
    needed = ["arrondissement", "annee"]
    for col in needed:
        if col not in df.columns:
            raise ValueError(f"❌ Colonne manquante : {col}")

    # Compter le nombre de programmes de logement social
    grouped = (
        df.groupby(["arrondissement", "annee"])
        .size()
        .reset_index(name="nb_programmes")
    )

    # Sauvegarde
    output = GOLD / "logements_sociaux.csv"
    grouped.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_logements_sociaux()
