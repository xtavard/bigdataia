
# --------------------------------------------------
# Script de génération des données référentielles
# du cas URBAN & CO
# --------------------------------------------------



import csv
from pathlib import Path

# --------------------------------------------------
# Répertoire de sortie
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data"/"referentiels"

OUTPUT_DIR.mkdir(parents=True,exist_ok=True)


# --------------------------------------------------
# Référentiel des catégories et sous-catégories 
# de produits
# --------------------------------------------------

catalogue = {
    "Mobilier salon" : [
         "Canapés",
         "Fauteuils",
         "Tables basses",
         "Meubles TV",
         "Bibliothèques",
    ],
    "Chambre": [
        "Lits",
        "Matelas",
        "Chevets",
        "Armoires",
        "Commodes",
    ],
    "Cuisine & repas": [
        "Tables",
        "Chaises",
        "Tabourets",
        "Rangements cuisine",
        "Accessoires repas",
    ],
    "Décoration": [
        "Vases",
        "Cadres",
        "Miroirs",
        "Objets décoratifs",
        "Horloges",
    ],
    "Éclairage": [
        "Lampes à poser",
        "Lampadaires",
        "Suspensions",
        "Appliques",
        "Éclairage extérieur",
    ],
    "Textile maison": [
        "Coussins",
        "Plaids",
        "Rideaux",
        "Linge de lit",
        "Linge de bain",
    ],
    "Rangement": [
        "Étagères",
        "Boîtes",
        "Paniers",
        "Dressings",
        "Rangements modulaires",
    ],
    "Petit électroménager": [
        "Café",
        "Petit-déjeuner",
        "Cuisine",
        "Entretien",
        "Confort",
    ],
    "Jardin & extérieur": [
        "Mobilier jardin",
        "Barbecue",
        "Pots et jardinières",
        "Éclairage jardin",
        "Accessoires extérieur",
    ],
    "Bureau & télétravail": [
        "Bureaux",
        "Chaises de bureau",
        "Rangements bureau",
        "Lampes de bureau",
        "Accessoires bureau",
    ],
}
   

# --------------------------------------------------
# Construction des données
# --------------------------------------------------
categories = []
sous_categories = []

numero_sous_categorie = 1

for numero_categorie, (categorie,sous_cats) in enumerate (catalogue.items(), start=1) :
    categorie_id = f"CAT{numero_categorie:02d}"

    categories.append({
            "categorie_id" : categorie_id,
            "categorie": categorie
        })

    for sous_categorie in sous_cats :
        sous_categorie_id = f"SC{numero_sous_categorie:03d}"
        sous_categories.append({
            "sous_categorie_id" : sous_categorie_id,
            "categorie_id": categorie_id,
            "sous_categorie":sous_categorie
            })
        numero_sous_categorie +=1
# --------------------------------------------------
# Ecriture de categories.csv
# --------------------------------------------------

with open(
    OUTPUT_DIR / "categories.csv",
    "w",
    newline="",
    encoding="utf-8-sig",
) as fichier :

    writer = csv.DictWriter(
        fichier,
        fieldnames = ["categorie_id","categorie"],
        delimiter =";"
    )
    writer.writeheader()
    writer.writerows(categories)

# --------------------------------------------------
# Écriture de sous_categories.csv
# --------------------------------------------------

with open(
    OUTPUT_DIR / "sous_categories.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as fichier:

    writer = csv.DictWriter(
        fichier,
        fieldnames=[
            "sous_categorie_id",
            "categorie_id",
            "sous_categorie"
        ],
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(sous_categories)


# --------------------------------------------------
# Bilan
# --------------------------------------------------

print("Référentiels créés avec succès.")
print(f"Catégories : {len(categories)}")
print(f"Sous-catégories : {len(sous_categories)}")
print(f"Dossier : {OUTPUT_DIR}")


