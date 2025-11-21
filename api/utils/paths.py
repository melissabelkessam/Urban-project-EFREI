from pathlib import Path
# Chemin du dossier racine du projet
ROOT = Path(__file__).resolve().parents[2]

# Chemin vers le dossier data
DATA = ROOT / "data"

# Dossiers Gold et Silver
GOLD = DATA / "Gold"
SILVER = DATA / "Silver"
