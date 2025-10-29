import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables depuis le fichier .env
load_dotenv()

# Lire les variables d'environnement
BASE_URL = os.getenv("PARIS_OD_API_BASE")
DATASET = os.getenv("PARIS_OD_DATASET")

# Préparer les paramètres de la requête API
params = {
    "dataset": DATASET,
    "rows": 50,
    "timezone": "Europe/Paris"
}

# Appel à l'API
response = requests.get(BASE_URL, params=params)
data = response.json()

# Définir le chemin du dossier Bronze
bronze_path = Path(__file__).resolve().parents[2] / "data" / "Bronze"
bronze_path.mkdir(parents=True, exist_ok=True)

# Sauvegarder les données brutes en JSON
output_file = bronze_path / "arrondissements_raw.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Données enregistrées dans :", output_file)
