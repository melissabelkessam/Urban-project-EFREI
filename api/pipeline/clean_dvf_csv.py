import pandas as pd
import csv

# --- Fichier source ---
fichier = "data/Bronze/dvf.csv"
fichier_sortie = "data/silver/dvf.csv"

# --- Étape 1 : Détection automatique du dialecte CSV ---
with open(fichier, "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    dialect = csv.Sniffer().sniff(sample)
    sep = dialect.delimiter
    print(f"✅ Séparateur détecté : {repr(sep)}")

# --- Étape 2 : Lecture robuste du fichier ---
df = pd.read_csv(
    fichier,
    sep=sep,
    encoding="utf-8-sig",
    quotechar='"',
    dtype=str,
    keep_default_na=False,
    on_bad_lines='skip',  # ignore les lignes cassées
    engine="python"
)

# --- Étape 3 : Nettoyage basique ---
# Suppression espaces inutiles
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Conversion des types principaux
colonnes_numeriques = [
    "valeur_fonciere", "surface_reelle_bati", "nombre_pieces_principales",
    "surface_terrain", "longitude", "latitude"
]

for col in colonnes_numeriques:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col].str.replace(",", "."), errors="coerce")

# --- Étape 4 : Infos générales ---
print(df.head(3))
print(df.dtypes)
print(f"✅ Nombre de lignes : {len(df)}")
print(f"✅ Nombre de colonnes : {len(df.columns)}")

# --- Étape 5 : Sauvegarde ---
df.to_csv(fichier_sortie, index=False, encoding="utf-8-sig")
print(f"✅ Fichier nettoyé sauvegardé dans {fichier_sortie}")
