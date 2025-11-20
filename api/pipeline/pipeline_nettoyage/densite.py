import pandas as pd

# --- Fichiers source et sortie ---
fichier = "data/silver/delinquance_paris.csv"
fichier_sortie = "data/silver/densite_paris.csv"

# Lecture du CSV
df = pd.read_csv(fichier, sep=",", encoding="utf-8-sig")


# Surface des arrondissements en km²
surface_arrondissements = {
    1: 1.83, 2: 0.99, 3: 1.17, 4: 1.60, 5: 2.54, 6: 2.15, 7: 4.09,
    8: 3.88, 9: 2.18, 10: 2.89, 11: 3.67, 12: 6.38, 13: 7.15, 14: 5.62,
    15: 8.50, 16: 16.34, 17: 5.67, 18: 6.01, 19: 6.79, 20: 5.98
}

# Ajouter numéro arrondissement à partir du code INSEE
df["arrondissement"] = df["CODGEO_2025"].astype(str).str[2:4].astype(int)

# Calcul densité
df["densite_hab_km2"] = df.apply(
    lambda x: x["insee_pop"] / surface_arrondissements.get(x["arrondissement"], 1),
    axis=1
)

# Garder uniquement les colonnes souhaitées
df_final = df[["CODGEO_2025", "arrondissement", "insee_pop", "densite_hab_km2", "annee"]]
# Sauvegarde dans un nouveau fichier CSV
df_final.to_csv(fichier_sortie, index=False, encoding="utf-8-sig")

