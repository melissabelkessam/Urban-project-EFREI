import requests
import json
from pathlib import Path

print("⏳ Collecte espaces verts OpenData Paris...")

url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/espaces_verts/records"
all_records = []
offset = 0
limit = 100

while True:
    params = {"limit": limit, "offset": offset}
    r = requests.get(url, params=params)
    data = r.json()
    results = data.get("results", [])
    if not results:
        break
    all_records.extend(results)
    offset += limit
    total = data.get("total_count", 0)
    if offset >= total or offset >= 10000:
        break

bronze_path = Path(__file__).resolve().parents[2] / "data" / "Bronze"
bronze_path.mkdir(parents=True, exist_ok=True)

with open(bronze_path / "espaces_verts.json", "w", encoding="utf-8") as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)

print(f"✅ {len(all_records)} espaces verts sauvegardés dans Bronze")