import requests
from pathlib import Path


# Définition du dossier Bronze (chemin absolu propre)
ROOT = Path(__file__).resolve().parents[2]
BRONZE = ROOT / "data" / "Bronze"
BRONZE.mkdir(parents=True, exist_ok=True)


# URLs des fichiers DVF
urls = {
    2022: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234844/valeursfoncieres-2022.txt.zip",
    2023: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234851/valeursfoncieres-2023.txt.zip",
    2024: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234857/valeursfoncieres-2024.txt.zip",
    2025: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234902/valeursfoncieres-2025-s1.txt.zip",
}


# Téléchargement de chaque fichier DVF
for year, url in urls.items():
    output_file = BRONZE / f"dvf_75_{year}.zip"
    print(f"⏳ Téléchargement DVF {year}...")

    try:
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✅ Fichier {year} enregistré dans : {output_file}")

        else:
            print(f"⚠️ Erreur {response.status_code} pour {year} (url : {url})")

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {year} : {e}")


print("\n🏁 Téléchargement DVF terminé avec succès !")
