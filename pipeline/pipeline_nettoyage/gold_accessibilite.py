import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Détection de la racine du projet
# (gold_accessibilite.py → pipeline_nettoyage → pipeline → racine)
# -----------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]   # ✔️ bon emplacement

DATA = ROOT / "data"
SILVER = DATA / "Silver"
GOLD = DATA / "Gold"


def build_accessibilite():
    print("🔄 Construction de l'indicateur : accessibilité prix/revenu...")

    # Charger prix/m2 (Gold)
    prix = pd.read_csv(GOLD / "prix_m2_par_arrondissement.csv")

    # Charger revenus (Silver)
    revenus = pd.read_csv(SILVER / "revenus_paris.csv")

    # -----------------------------------------------------
    # 🔧 Conversion en numérique
    # -----------------------------------------------------
    for col in ["arrondissement", "annee"]:
        prix[col] = pd.to_numeric(prix[col], errors="coerce")
        revenus[col] = pd.to_numeric(revenus[col], errors="coerce")

    prix.dropna(subset=["arrondissement", "annee"], inplace=True)
    revenus.dropna(subset=["arrondissement", "annee"], inplace=True)

    prix["arrondissement"] = prix["arrondissement"].astype(int)
    prix["annee"] = prix["annee"].astype(int)

    revenus["arrondissement"] = revenus["arrondissement"].astype(int)
    revenus["annee"] = revenus["annee"].astype(int)

    # -----------------------------------------------------
    # 🔗 Fusion arrondissement + année
    # -----------------------------------------------------
    merged = prix.merge(revenus, on=["arrondissement", "annee"], how="left")

    if merged["revenu_median"].isna().sum() > 0:
        print("⚠️ Revenus manquants pour certaines combinaisons arrondissement/année")

    # -----------------------------------------------------
    # 📊 Calcul ratio prix/revenu
    # -----------------------------------------------------
    merged["ratio_prix_revenu"] = (
        merged["prix_m2_median"] / merged["revenu_median"]
    )

    # -----------------------------------------------------
    # 💾 Sauvegarde Gold
    # -----------------------------------------------------
    output = GOLD / "accessibilite.csv"
    merged.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"✅ Fichier GOLD créé : {output}")


if __name__ == "__main__":
    build_accessibilite()
