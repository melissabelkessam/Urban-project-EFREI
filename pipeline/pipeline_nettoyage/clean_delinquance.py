import pandas as pd
import csv
import io
from pathlib import Path

# --- Définition des chemins absolus ---
ROOT = Path(__file__).resolve().parents[2]    # remonte jusqu’à "URBAN DATA EFREI"
BRONZE = ROOT / "data" / "Bronze"
SILVER = ROOT / "data" / "Silver"

fichier = BRONZE / "delinquance_paris.csv"
fichier_sortie = SILVER / "delinquance_paris.csv"

# --- Étape 1 : Lecture brute et réparation des guillemets doublés ---
with open(fichier, "r", encoding="utf-8-sig") as f:
    contenu = f.read()

# Correction des doubles guillemets
contenu = contenu.replace('""', '"')

# --- Étape 2 : Détection du séparateur ---
try:
    dialect = csv.Sniffer().sniff(contenu[:2048])
    sep = dialect.delimiter
except Exception:
    sep = ","
print(f"✅ Séparateur détecté : {repr(sep)}")

# --- Étape 3 : Lecture du CSV ---
df = pd.read_csv(
    io.StringIO(contenu),
    sep=sep,
    encoding="utf-8-sig",
    quotechar='"',
    dtype=str,
    engine="python",
    on_bad_lines="skip"
)

# --- Étape 4 : Nettoyage des caractères ---
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
df = df.replace({'Ã©': 'é', 'Ã¨': 'è', 'Ã¢': 'â', 'Ã´': 'ô', 'Ãª': 'ê', 'Ã': 'à'}, regex=True)

# Conversion de "annee" en numérique
df["annee"] = pd.to_numeric(df["annee"], errors="coerce")

# --- Étape 5 : Conversion des types numériques ---
colonnes_numeriques = [
    "nombre", "taux_pour_mille", "insee_pop",
    "insee_pop_millesime", "insee_log", "insee_log_millesime"
]

for col in colonnes_numeriques:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".")
            .str.replace(" ", "")
            .replace("", None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Étape 6 : Filtrage ---
df = df[df["annee"] >= 2020]

# --- Étape 7 : Sauvegarde ---
SILVER.mkdir(parents=True, exist_ok=True)
df.to_csv(fichier_sortie, index=False, encoding="utf-8-sig")

print(f"✅ Fichier nettoyé sauvegardé dans {fichier_sortie}")
