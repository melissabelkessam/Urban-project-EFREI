import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Détecter correctement la racine du projet
# gold_pipeline.py → pipeline_nettoyage → pipeline → api → racine (3 parents)
# -----------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[3]

# Dossiers data
DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"


def build_prix_m2_par_arrondissement():
    print("🔄 Construction de l'indicateur : prix/m² médian...")

    dvf_path = SILVER / "dvf_ready.csv"

    # Charger DVF nettoyé
    df = pd.read_csv(dvf_path)

    # Calcul du prix au m²
    df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]

    # Groupby : arrondissement + année
    grouped = (
        df.groupby(["arrondissement", "annee"])
        .agg(
            prix_m2_median=("prix_m2", "median"),
            nb_ventes=("id_mutation", "count")
        )
        .reset_index()
    )

    # Sauvegarde dans data/Gold
    output_path = GOLD / "prix_m2_par_arrondissement.csv"
    grouped.to_csv(output_path, index=False)

    print(f"✅ Fichier GOLD créé : {output_path}")


if __name__ == "__main__":
    build_prix_m2_par_arrondissement()
