import pandas as pd
fichier = "data/silver/densite_paris.csv"
# Lecture du CSV
df = pd.read_csv(fichier, sep=",", encoding="utf-8-sig")
annee_min = int(df["annee"].min())
annee_max = int(df["annee"].max())

print("Première année :", annee_min)
print("Dernière année :", annee_max)