import pandas as pd

# Charger le DVF
df = pd.read_csv("../data/Silver/dvf_final.csv", low_memory=False)

# On ne garde que les ventes
df = df[df["nature_mutation"] == "Vente"]

# Convertir arrondissement en numérique
df["arrondissement"] = pd.to_numeric(df["arrondissement"], errors="coerce")

# Filtrer Paris 1 à 20
df = df[df["arrondissement"].between(1, 20)]

# Colonnes utiles
df = df[["arrondissement", "annee", "nombre_pieces_principales"]].dropna()

# Classification T1/T2/T3/T4+
def classify(x):
    try:
        x = int(x)
    except:
        return None
    if x == 1:
        return "T1"
    elif x == 2:
        return "T2"
    elif x == 3:
        return "T3"
    else:
        return "T4"

df["type_logement"] = df["nombre_pieces_principales"].apply(classify)

# Nombre de logements par type
counts = df.groupby(["arrondissement", "annee", "type_logement"]).size().reset_index(name="n")

# Total par année et arrondissement
totals = df.groupby(["arrondissement", "annee"]).size().reset_index(name="total")

# Merge + calcul %
merged = counts.merge(totals, on=["arrondissement", "annee"])
merged["part"] = (merged["n"] / merged["total"]) * 100

# Pivot final
pivot = merged.pivot_table(
    index=["arrondissement", "annee"],
    columns="type_logement",
    values="part",
    fill_value=0
).reset_index()

pivot = pivot.rename(columns={
    "T1": "part_T1",
    "T2": "part_T2",
    "T3": "part_T3",
    "T4": "part_T4"
})

# Export Silver
pivot.to_csv("../data/Silver/typologie_paris.csv", index=False)

print("Silver typologie OK ✔")
