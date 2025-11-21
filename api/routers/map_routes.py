from fastapi import APIRouter
from services.map_service import load_arrondissements

router = APIRouter()

@router.get("/arrondissements")
def arrondissements():
    return load_arrondissements()
