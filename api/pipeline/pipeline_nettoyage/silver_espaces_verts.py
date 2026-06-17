import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRONZE = ROOT / "data" / "Bronze"
SILVER = ROOT / "data" / "Silver"

with open(BRONZE / "espaces_verts.json", encoding="utf-8") as f:
    records = json.load(f)

rows = []
for r in records:
    cp = str(r.get("adresse_codepostal", "")).strip()
    # Prendre surface_totale_reelle, sinon poly_area
    area = r.get("surface_totale_reelle") or r.get("poly_area") or 0
    if cp.startswith("75") and len(cp) == 5 and area and area > 0:
        try:
            arr = int(cp[3:5])
            if 1 <= arr <= 20:
                rows.append({"arrondissement": arr, "superficie_m2": float(area)})
        except:
            pass

df = pd.DataFrame(rows)
print(f"Lignes trouvées: {len(df)}")
print("Arrondissements:", sorted(df['arrondissement'].unique()))
df.to_csv(SILVER / "espaces_verts_clean.csv", index=False)
print("✅ Silver espaces verts sauvegardé")