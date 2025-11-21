import pandas as pd

# Charger Silver
df = pd.read_csv("../data/Silver/delinquance_paris.csv")

# Extraire le numéro d'arrondissement : 
# CODGEO_2025 contient un code INSEE comme 75101, 75115 etc.
df["arrondissement"] = df["CODGEO_2025"].astype(str).str[-2:].astype(int)

# Garder seulement les colonnes utiles
df = df[["arrondissement", "annee", "nombre"]]

# Agréger : somme de tous les délits par arrondissement et année
df_agg = df.groupby(["arrondissement", "annee"])["nombre"].sum().reset_index()

# Normalisation par année (score entre 0 et 10)
df_agg["score_delinquance"] = df_agg.groupby("annee")["nombre"].transform(
    lambda x: (x / x.max()) * 10
).round(1)

# Colonnes finales
df_final = df_agg[["arrondissement", "annee", "score_delinquance"]]

# Export vers Gold
df_final.to_csv("../data/Gold/delinquance.csv", index=False)

print("Gold délinquance : OK ✔")
