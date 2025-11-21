import pandas as pd

df = pd.read_csv("../data/Silver/densite_paris.csv")

# On garde TOUTES LES ANNÉES du Silver !!
df = df[["arrondissement", "annee", "densite_hab_km2"]]

df.to_csv("../data/Gold/densite.csv", index=False)
print("Gold densité OK")
