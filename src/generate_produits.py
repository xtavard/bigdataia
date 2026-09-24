
# --------------------------------------------------
# Script de génération des données référentielles
# sur les produits
# du cas URBAN & CO
# --------------------------------------------------



import csv
import json
import random
from pathlib import Path
import ollama


# --------------------------------------------------
# configuration 
# --------------------------------------------------

NB_PRODUITS = 50

random.seed(42)


# --------------------------------------------------
# Répertoire de sortie
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
REF_DIR = BASE_DIR / "data" / "referentiels"
OUTPUT_DIR = BASE_DIR / "data"/"produits"
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)


# --------------------------------------------------
# Lecture générique d'un CSV
# --------------------------------------------------

def lire_csv(nom_fichier):

    with open(
        REF_DIR / nom_fichier,
        "r",
        encoding="utf-8-sig"
    ) as fichier:

        return list(
            csv.DictReader(
                fichier,
                delimiter=";"
            )
        )


# --------------------------------------------------
# Chargement des référentiels
# --------------------------------------------------

categories = lire_csv("categories.csv")
sous_categories = lire_csv("sous_categories.csv")
marques = lire_csv("marques.csv")
fournisseurs = lire_csv("fournisseurs.csv")
categorie_marques = lire_csv("categorie_marque.csv")
categorie_fournisseurs = lire_csv("categorie_fournisseur.csv")

# Dictionnaires permettant de retrouver rapidement
# les informations à partir d'un ID

categories_dict = {
    x["categorie_id"]: x
    for x in categories
}

sous_categories_dict = {
    x["sous_categorie_id"]: x
    for x in sous_categories
}

marques_dict = {
    x["marque_id"]: x
    for x in marques
}

fournisseurs_dict = {
    x["fournisseur_id"]: x
    for x in fournisseurs
}



# --------------------------------------------------
# Génération des caractéristiques sémantiques
# des produits
#  par QWEN
# --------------------------------------------------
def generer_semantique_produit (categorie, sous_categorie,marque):
    prompt=f"""
    Tu génères une fiche produit pour l'entreprise fictive 
    URBAN & CO, spécialisée dans l'équipement de la maison.

    Catégorie : {categorie}
    Sous-catégorie : {sous_categorie}
    Marque : {marque}

    Génère un produit réaliste et commercialement crédible

    Retourne UNIQUEMENT un objet JSON contenant exactement les champs suivants :
    nom_produit
    description
    matiere_principale
    couleur_principale
    style

    Contraintes : 
    - le nom doit être court (moins de 20 caractères) et commercial 
    - ne répète pas le nom de la marque dans nom_produit ;
    - la description doit faire une ou deux phrases ;
    - la matière doit être cohérente avec le produit ;
    - la couleur doit être plausible ;
    - le style doit appartenir à une esthétique d'équipement de la maison ;
    - n'ajoute aucun autre champ
    """

    response = ollama.chat(
            model = "qwen2.5:7b", 
            messages =[
                {
                    "role":"user",
                    "content": prompt
                }],
            format="json",
            options={
                "temperature":0.8
                }
            )
    return json.loads(response["message"]["content"])


produits = []

for numero in range(1, NB_PRODUITS + 1):

    # -----------------------------
    # Choix d'une sous-catégorie
    # au hasard
    # -----------------------------

    sous_cat = random.choice(sous_categories)
    sous_categorie_id = sous_cat["sous_categorie_id"]
    categorie_id = sous_cat["categorie_id"]
  
    categorie = categories_dict[categorie_id]["categorie"]
    sous_categorie = sous_cat["sous_categorie"]

    # -----------------------------
    # Marques compatibles
    # -----------------------------

    marques_possibles = [
        relation["marque_id"]
        for relation in categorie_marques
        if relation["categorie_id"] == categorie_id
    ]

    marque_id = random.choice(marques_possibles)

    marque = marques_dict[marque_id]["marque"]


    # -----------------------------
    # Fournisseurs compatibles
    # -----------------------------

    fournisseurs_possibles = [
        relation["fournisseur_id"]
        for relation in categorie_fournisseurs
        if relation["categorie_id"] == categorie_id
    ]

    fournisseur_id = random.choice(fournisseurs_possibles)

    # -----------------------------
    # Appel de Qwen
    # -----------------------------

    print(
        f"Génération produit "
        f"{numero}/{NB_PRODUITS} : "
        f"{sous_categorie}"
    )

    semantique = generer_semantique_produit(
        categorie,
        sous_categorie,
        marque
    )


    # -----------------------------
    # Construction du produit
    # -----------------------------

    produit = {
        "produit_id": f"P{numero:05d}",

        "categorie_id":categorie_id,

        "sous_categorie_id":sous_categorie_id,

        "marque_id": marque_id,

        "fournisseur_id": fournisseur_id,

        "nom_produit": semantique["nom_produit"],

        "description":semantique["description"],

        "matiere_principale": semantique["matiere_principale"],

        "couleur_principale": semantique["couleur_principale"],

        "style": semantique["style"]
    }

    produits.append(produit)


# --------------------------------------------------
# Export CSV
# --------------------------------------------------

fichier_sortie = (
    OUTPUT_DIR / "produits.csv"
)

with open(
    fichier_sortie,
    "w",
    newline="",
    encoding="utf-8-sig"
) as fichier:

    champs = [
        "produit_id",
        "categorie_id",
        "sous_categorie_id",
        "marque_id",
        "fournisseur_id",
        "nom_produit",
        "description",
        "matiere_principale",
        "couleur_principale",
        "style"
    ]

    writer = csv.DictWriter(
        fichier,
        fieldnames=champs,
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(produits)


print()
print("==============================")
print("GÉNÉRATION TERMINÉE")
print("==============================")
print(f"Produits générés : {len(produits)}")
print(f"Fichier : {fichier_sortie}")

