import pandas as pd
from utils.paths import SILVER

def load_arrondissements():
    """Charge les arrondissements nettoyés depuis le dossier SILVER."""
    file_path = SILVER / "arrondissements_clean.csv"
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")
