import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Détecter correctement la racine du projet
# silver_typologie.py → pipeline_nettoyage → pipeline → racine
# -----------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
SILVER = DATA / "Silver"


def clean_typologie():
    print("🔄 Nettoyage typologie DVF...")

    # Charger DVF Silver
    df = pd.read_csv(SILVER / "dvf_final.csv", low_memory=False, encoding="utf-8-sig")

    # Ne garder que les ventes
    df = df[df["nature_mutation"] == "Vente"]

    # Convertir arrondissement
    df["arrondissement"] = pd.to_numeric(df["arrondissement"], errors="coerce")
    df = df[df["arrondissement"].between(1, 20)]

    # Colonnes utiles
    df = df[["arrondissement", "annee", "nombre_pieces_principales"]].dropna()

    # Classification T1–T4
    def classify(x):
        try:
            x = int(x)
        except:
            return None
        if x == 1:
            return "T1"
        elif x == 2:
            return "T2"
        elif x == 3:
            return "T3"
        else:
            return "T4"

    df["type_logement"] = df["nombre_pieces_principales"].apply(classify)

    # Nombre de logements par type
    counts = df.groupby(["arrondissement", "annee", "type_logement"]).size().reset_index(name="n")

    # Totaux par arrondissement/année
    totals = df.groupby(["arrondissement", "annee"]).size().reset_index(name="total")

    # Merge + calcul %
    merged = counts.merge(totals, on=["arrondissement", "annee"])
    merged["part"] = (merged["n"] / merged["total"]) * 100

    # Pivot final
    pivot = merged.pivot_table(
        index=["arrondissement", "annee"],
        columns="type_logement",
        values="part",
        fill_value=0
    ).reset_index()

    pivot = pivot.rename(columns={
        "T1": "part_T1",
        "T2": "part_T2",
        "T3": "part_T3",
        "T4": "part_T4"
    })

    # Export Silver
    output_path = SILVER / "typologie_paris.csv"
    pivot.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Silver typologie créé → {output_path}")


if __name__ == "__main__":
    clean_typologie()
