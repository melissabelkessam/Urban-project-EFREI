import pandas as pd
from utils.paths import GOLD

def load_gold(filename: str):
    """Charge un fichier CSV depuis le dossier GOLD."""
    file_path = GOLD / filename
    return pd.read_csv(file_path).to_dict(orient="records")
