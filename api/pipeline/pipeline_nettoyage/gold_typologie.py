import pandas as pd
from pathlib import Path

# Chemins adaptés à ta structure
ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"

def build_typologie_logements():
    print("🔄 Construction de l'indicateur : typologie des logements...")

    df = pd.read_csv(SILVER / "dvf_ready.csv")

    # Filtrer seulement Maison/Appartement si tu veux
    df = df[df["type_local"].isin(["Appartement", "Maison"])]

    # Grouper par arrondissement, année, type, nb pièces
    grouped = (
        df.groupby(["arrondissement", "annee", "type_local", "nombre_pieces_principales"])
        .agg(
            count=("id_mutation", "count")
        )
        .reset_index()
    )

    # Sauvegarde
    output = GOLD / "typologie_logements.csv"
    grouped.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_typologie_logements()
python api/pipeline/pipeline_nettoyage/gold_typologie.py
