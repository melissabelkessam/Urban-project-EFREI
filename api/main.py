from fastapi import FastAPI, Query, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from typing import Optional

app = FastAPI(title="Urban Data Explorer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GOLD = DATA / "Gold"
SILVER = DATA / "Silver"

API_KEY = "urban-data-explorer-2024"


def load_gold(name: str):
    return pd.read_csv(GOLD / name)


def check_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Clé API invalide. Fournir le header X-API-Key.")
    return x_api_key


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "API Urban Data Explorer fonctionne !",
        "version": "1.0.0",
        "endpoints": ["/prix_m2", "/logements_sociaux", "/delinquance", "/densite",
                      "/espaces_verts", "/qualite_air", "/typologie", "/arrondissements",
                      "/timeline", "/comparaison", "/admin/status"]
    }


@app.get("/admin/status")
def admin_status(x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    return {
        "status": "ok",
        "message": "Accès admin autorisé",
        "tables": 7,
        "sources": ["DVF data.gouv", "OpenData Paris", "INSEE", "SSMSI", "Airparif"],
        "arrondissements": 20,
        "annees": "2020-2024"
    }


@app.get("/prix_m2")
def prix_m2(annee: Optional[int] = None, arrondissement: Optional[int] = None):
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


@app.get("/espaces_verts")
def espaces_verts(arrondissement: Optional[int] = None):
    df = load_gold("espaces_verts.csv")
    if arrondissement:
        df = df[df["arrondissement"] == arrondissement]
    return df.to_dict(orient="records")


@app.get("/qualite_air")
def qualite_air(arrondissement: Optional[int] = None):
    df = load_gold("qualite_air.csv")
    if arrondissement:
        df = df[df["arrondissement"] == arrondissement]
    return df.to_dict(orient="records")


@app.get("/arrondissements")
def arrondissements():
    df = pd.read_csv(SILVER / "arrondissements_clean.csv")
    return df.to_dict(orient="records")


@app.get("/timeline")
def timeline(arr: int = Query(..., description="Code arrondissement (1-20)")):
    df = load_gold("prix_m2_par_arrondissement.csv")
    df_arr = df[df["arrondissement"] == arr].sort_values("annee")
    if df_arr.empty:
        return {"arrondissement": arr, "data": []}
    df_arr = df_arr.copy()
    df_arr["variation_pct"] = df_arr["prix_m2_median"].pct_change() * 100
    df_arr["variation_pct"] = df_arr["variation_pct"].round(1).fillna(0)
    return {
        "arrondissement": arr,
        "data": df_arr[["annee", "prix_m2_median", "nb_ventes", "variation_pct"]].to_dict(orient="records")
    }


@app.get("/comparaison")
def comparaison(
    arr1: int = Query(...),
    arr2: int = Query(...),
    annee: Optional[int] = None
):
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
        ev = get_indicator("espaces_verts.csv", arr_code, None)
        typo = get_indicator("typologie_logements.csv", arr_code, annee)
        air = get_indicator("qualite_air.csv", arr_code, None)

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
            "espaces_verts": ev[0] if ev else None,
            "qualite_air": air[0] if air else None,
            "typologie": typo[0] if typo else None,
            "timeline": timeline_data,
        }

    return {
        "annee": annee,
        "arrondissement_1": build_arr_data(arr1),
        "arrondissement_2": build_arr_data(arr2),
    }