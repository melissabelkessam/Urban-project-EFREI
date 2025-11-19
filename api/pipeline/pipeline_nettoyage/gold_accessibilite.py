import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Détection de la racine du projet
# (gold_accessibilite.py → pipeline_nettoyage → pipeline → api → racine)
# -----------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = ROOT_DIR / "data"
SILVER = DATA_DIR / "Silver"
GOLD = DATA_DIR / "Gold"


def build_accessibilite():
    print("🔄 Construction de l'indicateur : accessibilité prix/revenu...")

    # Charger prix/m2 (Gold)
    prix = pd.read_csv(GOLD / "prix_m2_par_arrondissement.csv")

    # Charger revenus (Silver)
    revenus = pd.read_csv(SILVER / "revenus_paris.csv")

    # -----------------------------------------------------
    # 🔧 Nettoyage automatique : conversion en numérique
    # -----------------------------------------------------
    for col in ["arrondissement", "annee"]:
        prix[col] = pd.to_numeric(prix[col], errors="coerce")
        revenus[col] = pd.to_numeric(revenus[col], errors="coerce")

    # Supprimer les lignes invalides
    prix = prix.dropna(subset=["arrondissement", "annee"])
    revenus = revenus.dropna(subset=["arrondissement", "annee"])

    # Convertir en entiers
    prix["arrondissement"] = prix["arrondissement"].astype(int)
    prix["annee"] = prix["annee"].astype(int)

    revenus["arrondissement"] = revenus["arrondissement"].astype(int)
    revenus["annee"] = revenus["annee"].astype(int)

    # -----------------------------------------------------
    # 🔗 Fusion arrondissement + année
    # -----------------------------------------------------
    merged = prix.merge(revenus, on=["arrondissement", "annee"], how="left")

    # Vérifier si des revenus manquent
    if merged["revenu_median"].isna().sum() > 0:
        print("⚠️ Attention : revenus manquants pour certains arrondissements/années")

    # -----------------------------------------------------
    # 📊 Calcul du ratio prix/revenu
    # -----------------------------------------------------
    merged["ratio_prix_revenu"] = merged["prix_m2_median"] / merged["revenu_median"]

    # -----------------------------------------------------
    # 💾 Sauvegarde Gold
    # -----------------------------------------------------
    output = GOLD / "accessibilite.csv"
    merged.to_csv(output, index=False)

    print(f"✅ Fichier GOLD créé : {output}")


if __name__ == "__main__":
    build_accessibilite()
