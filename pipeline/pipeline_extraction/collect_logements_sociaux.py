import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# API logements sociaux (OpenData Paris)
BASE_URL = os.getenv("LOGEMENTS_SOCIAUX_API_BASE")
DATASET = os.getenv("LOGEMENTS_SOCIAUX_DATASET")

params = {
    "dataset": DATASET,
    "rows": 2000,
    "timezone": "Europe/Paris"
}

print("⏳ Récupération des logements sociaux en cours...")

# Requête API
response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()

    # Définition du dossier Bronze
    ROOT = Path(__file__).resolve().parents[2]
    BRONZE = ROOT / "data" / "Bronze"
    BRONZE.mkdir(parents=True, exist_ok=True)

    # Fichier de sortie
    output_file = BRONZE / "logements_sociaux.json"

    # Sauvegarde JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Données sauvegardées dans : {output_file}")

else:
    print(f"❌ Erreur {response.status_code} lors de la requête à l'API.")
