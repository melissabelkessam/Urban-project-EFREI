from fastapi import APIRouter
from services.gold_service import load_gold

router = APIRouter()

@router.get("/prix_m2")
def prix_m2():
    return load_gold("prix_m2_par_arrondissement.csv")

@router.get("/typologie")
def typologie():
    return load_gold("typologie_logements.csv")

@router.get("/logements_sociaux")
def logements_sociaux():
    return load_gold("logements_sociaux.csv")

@router.get("/delinquance")
def delinquance():
    return load_gold("delinquance.csv")

@router.get("/densite")
def densite():
    return load_gold("densite.csv")

@router.get("/vacance")
def vacance():
    return load_gold("vacance.csv")

@router.get("/qualite_air")
def qualite_air():
    return load_gold("qualite_air.csv")
