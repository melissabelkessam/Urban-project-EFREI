from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from typing import Optional

app = FastAPI(title="Urban Data Explorer API", version="1.0.0")

# Autoriser les appels depuis le front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemins
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GOLD = DATA / "Gold"
SILVER = DATA / "Silver"


def load_gold(name: str):
    return pd.read_csv(GOLD / name)


# ─── ROOT ────────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"status": "ok", "message": "API Urban Data Explorer fonctionne !"}


# ─── ENDPOINTS DE BASE ────────────────────────────────────────────────────────
@app.get("/prix_m2")
def prix_m2(annee: Optional[int] = None, arrondissement: Optional[int] = None):
    """Prix m² médian. Filtrable par ?annee=2023 et/ou ?arrondissement=6"""
    df = load_gold("prix_m2_par_arrondissement.csv")
    if annee:
        df = df[df["annee"] == annee]
    if arrondissement:
        df = df[df["arrondissement"] == arrondissement]
    return df.to_dict(orient="records")


@app.get("/typologie")
def typologie(annee: Optional[int] = None):
    df = load_gold("typologie_logements.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/logements_sociaux")
def logements_sociaux(annee: Optional[int] = None):
    df = load_gold("logements_sociaux.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/delinquance")
def delinquance(annee: Optional[int] = None):
    df = load_gold("delinquance.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/densite")
def densite(annee: Optional[int] = None):
    df = load_gold("densite.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/vacance")
def vacance(annee: Optional[int] = None):
    df = load_gold("vacance.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/qualite_air")
def qualite_air(annee: Optional[int] = None):
    df = load_gold("qualite_air.csv")
    if annee:
        df = df[df["annee"] == annee]
    return df.to_dict(orient="records")


@app.get("/arrondissements")
def arrondissements():
    """Arrondissements avec coordonnées"""
    df = pd.read_csv(SILVER / "arrondissements_clean.csv")
    return df.to_dict(orient="records")


# ─── TIMELINE ────────────────────────────────────────────────────────────────
@app.get("/timeline")
def timeline(arr: int = Query(..., description="Code arrondissement (1-20)")):
    """
    Évolution historique du prix/m² pour un arrondissement donné.
    Exemple : /timeline?arr=6
    """
    df = load_gold("prix_m2_par_arrondissement.csv")
    df_arr = df[df["arrondissement"] == arr].sort_values("annee")

    if df_arr.empty:
        return {"arrondissement": arr, "data": []}

    # Calcul de la variation annuelle en %
    df_arr = df_arr.copy()
    df_arr["variation_pct"] = df_arr["prix_m2_median"].pct_change() * 100
    df_arr["variation_pct"] = df_arr["variation_pct"].round(1).fillna(0)

    return {
        "arrondissement": arr,
        "data": df_arr[["annee", "prix_m2_median", "nb_ventes", "variation_pct"]].to_dict(orient="records")
    }


# ─── COMPARAISON ─────────────────────────────────────────────────────────────
@app.get("/comparaison")
def comparaison(
    arr1: int = Query(..., description="Premier arrondissement"),
    arr2: int = Query(..., description="Deuxième arrondissement"),
    annee: Optional[int] = None
):
    """
    Compare deux arrondissements sur tous les indicateurs.
    Exemple : /comparaison?arr1=1&arr2=6&annee=2023
    """

    def get_indicator(csv_name: str, arr_code: int, year: Optional[int]):
        try:
            df = load_gold(csv_name)
            df_f = df[df["arrondissement"] == arr_code]
            if year:
                df_f = df_f[df_f["annee"] == year]
            return df_f.to_dict(orient="records")
        except Exception:
            return []

    def build_arr_data(arr_code: int):
        prix = get_indicator("prix_m2_par_arrondissement.csv", arr_code, annee)
        social = get_indicator("logements_sociaux.csv", arr_code, annee)
        delin = get_indicator("delinquance.csv", arr_code, annee)
        dens = get_indicator("densite.csv", arr_code, annee)
        vac = get_indicator("vacance.csv", arr_code, annee)
        typo = get_indicator("typologie_logements.csv", arr_code, annee)

        # Timeline des prix pour sparkline
        try:
            df_all = load_gold("prix_m2_par_arrondissement.csv")
            timeline_data = df_all[df_all["arrondissement"] == arr_code].sort_values("annee")[["annee", "prix_m2_median"]].to_dict(orient="records")
        except Exception:
            timeline_data = []

        return {
            "arrondissement": arr_code,
            "prix": prix[0] if prix else None,
            "logements_sociaux": social[0] if social else None,
            "delinquance": delin[0] if delin else None,
            "densite": dens[0] if dens else None,
            "vacance": vac[0] if vac else None,
            "typologie": typo[0] if typo else None,
            "timeline": timeline_data,
        }

    return {
        "annee": annee,
        "arrondissement_1": build_arr_data(arr1),
        "arrondissement_2": build_arr_data(arr2),
    }
