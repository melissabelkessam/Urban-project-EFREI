import requests
from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables du fichier .env
load_dotenv()

# Lire les variables d'environnement
BASE_URL = os.getenv("DVF_API_BASE")
CODE_DEPT = os.getenv("DVF_CODE_DEPT")

# Construire l'URL complète de l'API DVF
url = f"{BASE_URL}valeursfoncieres-2025-s1.txt.zip"




# Créer le dossier Bronze s'il n'existe pas
bronze_path = Path(__file__).resolve().parents[2] / "data" / "Bronze"
bronze_path.mkdir(parents=True, exist_ok=True)

# Définir le chemin du fichier de sortie
output_file = bronze_path / f"dvf_{CODE_DEPT}.zip"


# Télécharger le fichier CSV depuis l'API
print("⏳ Téléchargement des données DVF en cours...")
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"✅ Données DVF sauvegardées dans : {output_file}")
else:
    print(f"❌ Erreur {response.status_code} lors du téléchargement.")
