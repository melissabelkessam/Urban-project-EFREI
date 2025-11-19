import pandas as pd
from pathlib import Path

# Détecter la racine du projet automatiquement
# silver_pipeline.py → pipeline_nettoyage → pipeline → api → racine
ROOT_DIR = Path(__file__).resolve().parents[3]

# Dossiers data
DATA_DIR = ROOT_DIR / "data"
BRONZE = DATA_DIR / "Bronze"
SILVER = DATA_DIR / "Silver"


def clean_dvf():
    print("🔄 Nettoyage DVF...")

    dvf_path = SILVER / "dvf_final.csv"
    mapping_path = SILVER / "code_postal_arr.csv"

    # Charger DVF
    df = pd.read_csv(dvf_path)

    # Convertir les types
    df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
    df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
    df["date_mutation"] = pd.to_datetime(df["date_mutation"], errors="coerce")

    # Nettoyage de base
    df = df.dropna(subset=["valeur_fonciere", "surface_reelle_bati", "date_mutation"])
    df = df[df["surface_reelle_bati"] > 0]

    # Extraire l'année
    df["annee"] = df["date_mutation"].dt.year

    # Charger mapping code_postal -> arrondissement
    mapping = pd.read_csv(mapping_path)

    # Fusion DVF + mapping
    df = df.merge(mapping, on="code_postal", how="left")

    # Alerte si certaines lignes n'ont pas trouvé d'arrondissement
    if df["code_arrondissement"].isna().sum() > 0:
        print("⚠️ Certains codes postaux n'ont pas trouvé leur arrondissement !")

    # Renommer la colonne
    df = df.rename(columns={"code_arrondissement": "arrondissement"})

    # Sauvegarde du fichier Silver propre
    output_path = SILVER / "dvf_ready.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ DVF Silver nettoyé → {output_path}")


if __name__ == "__main__":
    clean_dvf()
