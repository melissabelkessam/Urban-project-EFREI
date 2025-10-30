import requests
from pathlib import Path


bronze_path = Path(__file__).resolve().parents[2] / "data" / "Bronze"
bronze_path.mkdir(parents=True, exist_ok=True)


urls = {
    2022: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234844/valeursfoncieres-2022.txt.zip",
    2023: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234851/valeursfoncieres-2023.txt.zip",
    2024: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234857/valeursfoncieres-2024.txt.zip",
    2025: "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234902/valeursfoncieres-2025-s1.txt.zip",
}


for year, url in urls.items():
    output_file = bronze_path / f"dvf_75_{year}.zip"
    print(f"⏳ Téléchargement DVF {year} ...")

    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✅ Fichier {year} enregistré dans {output_file}")
        else:
            print(f"⚠️ Erreur {response.status_code} pour {year}")
    except Exception as e:
        print(f"❌ Erreur {year} :", e)

print("\n🏁 Téléchargement DVF terminé avec succès !")
