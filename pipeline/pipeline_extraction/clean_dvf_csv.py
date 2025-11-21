from pathlib import Path

# Définir le chemin du dossier Bronze
ROOT = Path(__file__).resolve().parents[2]   # remonte jusqu'à "URBAN DATA EFREI"
BRONZE = ROOT / "data" / "Bronze"

# --- Réparer le CSV avant de le lire ---
input_file = BRONZE / "dvf.csv"
output_file = BRONZE / "dvf_cleaned.csv"

with open(input_file, "r", encoding="utf-8-sig") as f:
    lignes = f.readlines()

# Supprimer les guillemets globaux des lignes
lignes_nettoyees = [ligne.strip().strip('"') + "\n" for ligne in lignes]

# Sauvegarde du fichier nettoyé
with open(output_file, "w", encoding="utf-8-sig") as f:
    f.writelines(lignes_nettoyees)

print(f"✅ Fichier réparé : {output_file}")
