from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routers
from routers import gold_routes, map_routes


app = FastAPI(
    title="Urban Data Explorer API",
    description="API pour explorer les données urbaines (arrondissements, prix, typologie, etc.)",
    version="1.0.0"
)

# ----- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- ROUTE D’ACCUEIL -----
@app.get("/")
def home():
    return {"status": "ok", "message": "API Urban Data Explorer fonctionne !"}

# ----- INCLUSION DES ROUTERS -----
app.include_router(gold_routes.router)
app.include_router(map_routes.router)
