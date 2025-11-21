import pandas as pd

df = pd.read_csv("../data/Silver/vacance_paris.csv")

df = df[["arrondissement", "annee", "taux_vacance"]]

df.to_csv("../data/Gold/vacance.csv", index=False)

print("Gold vacance OK")
