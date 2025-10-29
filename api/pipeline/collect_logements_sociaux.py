import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Lire les variables depuis le fichier .env
BASE_URL = os.getenv("LOGEMENTS_SOCIAUX_API_BASE")
DATASET = os.getenv("LOGEMENTS_SOCIAUX_DATASET")

# Paramètres de la requête
params = {
    "dataset": DATASET,
    "rows": 2000,  # nombre de lignes à récupérer
    "timezone": "Europe/Paris"
}

# Faire la requête à l'API
print("⏳ Récupération des logements sociaux en cours...")
response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()

    # Créer le dossier Bronze s'il n'existe pas
    bronze_path = Path(__file__).resolve().parents[2] / "data" / "Bronze"
    bronze_path.mkdir(parents=True, exist_ok=True)

    # Sauvegarder les données brutes en JSON
    output_file = bronze_path / "logements_sociaux.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Données sauvegardées dans : {output_file}")
else:
    print(f"❌ Erreur {response.status_code} lors de la requête à l'API.")
