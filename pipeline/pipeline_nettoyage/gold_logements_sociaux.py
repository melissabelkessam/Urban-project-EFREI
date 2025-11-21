import pandas as pd
from pathlib import Path

# --- Définition correcte de la racine du projet ---
# gold_logements_sociaux.py → pipeline_nettoyage → pipeline → racine
ROOT = Path(__file__).resolve().parents[2]   # ✔️ CORRECT

DATA = ROOT / "data"
SILVER = DATA / "Silver"
GOLD = DATA / "Gold"

def build_logements_sociaux():
    print("🔄 Construction de l'indicateur : logements sociaux (programmes)…")

    # Charger fichier Silver
    df = pd.read_csv(SILVER / "logements_sociaux_clean.csv", encoding="utf-8-sig")

    # Vérifier colonnes nécessaires
    needed = ["arrondissement", "annee"]
    for col in needed:
        if col not in df.columns:
            raise ValueError(f"❌ Colonne manquante : {col}")

    # Compter le nombre de programmes par arrondissement et année
    grouped = (
        df.groupby(["arrondissement", "annee"])
        .size()
        .reset_index(name="nb_programmes")
    )

    # Sauvegarde dans Gold
    output = GOLD / "logements_sociaux.csv"
    GOLD.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"✅ Fichier GOLD créé : {output}")

if __name__ == "__main__":
    build_logements_sociaux()
