from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI()

# Autoriser les appels depuis le front (fichiers HTML/JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux restreindre plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# chemins
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GOLD = DATA / "Gold"
SILVER = DATA / "Silver"


def load_gold(name: str):
    return pd.read_csv(GOLD / name).to_dict(orient="records")


@app.get("/")
def home():
    return {"status": "ok", "message": "API Urban Data Explorer fonctionne !"}


# ---------- endpoints GOLD ----------
@app.get("/prix_m2")
def prix_m2():
    return load_gold("prix_m2_par_arrondissement.csv")


@app.get("/typologie")
def typologie():
    return load_gold("typologie_logements.csv")


@app.get("/logements_sociaux")
def logements_sociaux():
    return load_gold("logements_sociaux.csv")


# @app.get("/accessibilite")
# def accessibilite():
#     return load_csv("accessibilite.csv")


@app.get("/delinquance")
def delinquance():
    return load_gold("delinquance.csv")


@app.get("/densite")
def densite():
    return load_gold("densite.csv")


@app.get("/vacance")
def vacance():
    return load_gold("vacance.csv")


@app.get("/qualite_air")
def qualite_air():
    return load_gold("qualite_air.csv")


# ---------- endpoint pour la carte : arrondissements + coords ----------
@app.get("/arrondissements")
def arrondissements():
    """
    Renvoie les arrondissements avec
    - code_arrondissement (1..20)
    - nom_officiel / nom
    - coord_x (lon) / coord_y (lat)
    """
    df = pd.read_csv(SILVER / "arrondissements_clean.csv")
    return df.to_dict(orient="records")
