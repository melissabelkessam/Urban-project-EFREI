import pandas as pd
import csv
import io

# --- Fichiers source et sortie ---
fichier = "data/Bronze/dvf_cleaned.csv"
fichier_sortie = "data/silver/dvf_final.csv"

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

# --- Étape 4 : Nettoyage léger ---
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df.replace({'Ã©': 'é', 'Ã¨': 'è', 'Ã¢': 'â', 'Ã´': 'ô', 'Ãª': 'ê', 'Ã': 'à'}, regex=True)

# --- Étape 5 : Conversion des types numériques ---
colonnes_numeriques = [
    "valeur_fonciere", "surface_reelle_bati", "nombre_pieces_principales",
    "surface_terrain", "longitude", "latitude"
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

if "date_mutation" in df.columns:
    df["date_mutation"] = pd.to_datetime(df["date_mutation"], errors="coerce")

# --- Étape 6 : Filtrage ---
df = df[df["valeur_fonciere"].notna() & (df["valeur_fonciere"] > 0)]
# --- Prix au m² ---
df['prix_m2'] = df['valeur_fonciere'] / df['surface_reelle_bati']
# --- Ajout d'année de mutation ---
df['annee'] = pd.to_datetime(df['date_mutation']).dt.year
# --- Ajout d'arrondissement ---
df['arrondissement'] = df['code_postal'].astype(str).str[-2:]

# --- Type simplifié du logement
df['type_local_simple'] = df['type_local'].str.capitalize()
# ---- Catégorie par nombre de pièces
def categorie_pieces(x):
    if x <= 2: return 'Petit'
    elif x <= 4: return 'Moyen'
    else: return 'Grand'

df['categorie_pieces'] = df['nombre_pieces_principales'].apply(categorie_pieces)

# --- Étape 7 : Résumé ---
print("\n🧾 Aperçu des données nettoyées :")
print(df.head(5))
print(f"\n✅ Nombre de lignes : {len(df)}")
print(f"✅ Nombre de colonnes : {len(df.columns)}")

# --- Étape 8 : Sauvegarde ---
df.to_csv(fichier_sortie, index=False, encoding="utf-8-sig")
print(f"✅ Fichier nettoyé sauvegardé dans {fichier_sortie}")
