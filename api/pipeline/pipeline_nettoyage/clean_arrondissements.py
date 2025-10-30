import json
import pandas as pd
from pathlib import Path

# --- chemins ---
raw_path = Path("data/Bronze/arrondissements_raw.json")
clean_path = Path("data/Silver/arrondissements_clean.csv")

# --- lecture du JSON brut ---
with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- extraction des enregistrements ---
records = data.get("records", [])

clean_data = []
for r in records:
    fields = r.get("fields", {})
    geom = fields.get("geom_x_y", [None, None])
    clean_data.append({
        "code_arrondissement": fields.get("c_ar"),
        "nom_officiel": fields.get("l_aroff"),
        "nom": fields.get("l_ar"),
        "surface_m2": fields.get("surface"),
        "coord_x": geom[1],
        "coord_y": geom[0]
    })

# --- conversion en DataFrame ---
df = pd.DataFrame(clean_data)

# --- nettoyage de base ---
df.drop_duplicates(inplace=True)
df.dropna(subset=["coord_x", "coord_y"], inplace=True)

# --- sauvegarde en CSV ---
clean_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(clean_path, index=False, encoding="utf-8")

print(f"✅ Données nettoyées sauvegardées dans {clean_path}")
