# --- Réparer le CSV avant de le lire ---
with open("data/Bronze/dvf.csv", "r", encoding="utf-8-sig") as f:
    lignes = f.readlines()

# On supprime les guillemets globaux de début et fin de ligne
lignes_nettoyees = [ligne.strip().strip('"') + "\n" for ligne in lignes]

# On sauvegarde un fichier corrigé temporaire
with open("data/Bronze/dvf_cleaned.csv", "w", encoding="utf-8-sig") as f:
    f.writelines(lignes_nettoyees)

print("✅ Fichier réparé : data/Bronze/dvf_cleaned.csv")
