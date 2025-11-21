import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()

# API OpenData Paris
BASE_URL = os.getenv("PARIS_OD_API_BASE")
DATASET = os.getenv("PARIS_OD_DATASET")

params = {
    "dataset": DATASET,
    "rows": 50,
    "timezone": "Europe/Paris"
}

# Appel API
response = requests.get(BASE_URL, params=params)

# Récupération JSON
data = response.json()

# Définition du dossier Bronze (chemin absolu PROPRE)
ROOT = Path(__file__).resolve().parents[2]
BRONZE = ROOT / "data" / "Bronze"
BRONZE.mkdir(parents=True, exist_ok=True)

# Fichier de sortie
output_file = BRONZE / "arrondissements_raw.json"

# Sauvegarde
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Données enregistrées dans : {output_file}")
