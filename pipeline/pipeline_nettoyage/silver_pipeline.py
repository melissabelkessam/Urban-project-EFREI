import pandas as pd
from pathlib import Path

# Détecter correctement la racine du projet
# silver_pipeline.py → pipeline_nettoyage → pipeline → racine
ROOT = Path(__file__).resolve().parents[2]   # ✔️ CORRECT

# Dossiers data
DATA = ROOT / "data"
BRONZE = DATA / "Bronze"
SILVER = DATA / "Silver"


def clean_dvf():
    print("🔄 Nettoyage DVF...")

    dvf_path = SILVER / "dvf_final.csv"
    mapping_path = SILVER / "code_postal_arr.csv"

    # Charger DVF
    df = pd.read_csv(dvf_path, encoding="utf-8-sig")

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
    mapping = pd.read_csv(mapping_path, encoding="utf-8-sig")

    # Fusion DVF + mapping
    df = df.merge(mapping, on="code_postal", how="left")

    # Alerte si certaines lignes n'ont pas trouvé d'arrondissement
    if df["code_arrondissement"].isna().sum() > 0:
        print("⚠️ Certains codes postaux n'ont PAS trouvé leur arrondissement !")

    # Renommer la colonne
    df = df.rename(columns={"code_arrondissement": "arrondissement"})

    # Sauvegarde du fichier Silver propre
    output_path = SILVER / "dvf_ready.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ DVF Silver nettoyé → {output_path}")


if __name__ == "__main__":
    clean_dvf()
