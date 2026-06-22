"""
Base NoSQL (TinyDB) — C1.2
Charge les données brutes semi-structurées (espaces verts avec géométries
imbriquées, champs hétérogènes selon la source) dans une vraie base
NoSQL orientée documents, sans schéma fixe imposé.
"""
import json
from pathlib import Path
from tinydb import TinyDB, Query

ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "data" / "Bronze"
NOSQL_DIR = ROOT / "data" / "nosql"
NOSQL_DIR.mkdir(exist_ok=True)

with open(BRONZE / "espaces_verts.json", encoding="utf-8") as f:
    records = json.load(f)

db = TinyDB(NOSQL_DIR / "espaces_verts_db.json")
table = db.table("espaces_verts")
table.truncate()
table.insert_multiple(records)

print(f"Documents inseres dans la base NoSQL (TinyDB): {len(table)}")
print(f"Fichier : {NOSQL_DIR / "espaces_verts_db.json"}")

EV = Query()
paris_5 = table.search(EV.adresse_codepostal == "75005")
print(f"Requete NoSQL - espaces verts du 5eme arrondissement (75005): {len(paris_5)} resultats")
if paris_5:
    sample = paris_5[0]
    print(f"Exemple: {sample.get("nom_ev")} - {sample.get("categorie")}")
