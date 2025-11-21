import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Détecter correctement la racine du projet
# gold_pipeline.py → pipeline_nettoyage → pipeline → racine (2 parents)
# -----------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]   # ✔️ CORRECT !

# Dossiers data
DATA = ROOT / "data"
SILVER = DATA / "Silver"
GOLD = DATA / "Gold"


def build_prix_m2_par_arrondissement():
    print("🔄 Construction de l'indicateur : prix/m² médian...")

    dvf_path = SILVER / "dvf_ready.csv"

    # Charger DVF nettoyé
    df = pd.read_csv(dvf_path, encoding="utf-8-sig")

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
    GOLD.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Fichier GOLD créé : {output_path}")


if __name__ == "__main__":
    build_prix_m2_par_arrondissement()
