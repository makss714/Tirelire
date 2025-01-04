import json

# Fonction pour créer un profil enfant
def creer_profil(nom, montant_depart, argent_poche, frequence, paypal=None, iban=None):
    enfant = {
        "nom": nom,
        "solde": montant_depart,
        "frequence": frequence,
        "paypal": paypal,
        "iban": iban,
        "historique": []
    }
    # Ajouter l'enfant au fichier JSON
    with open('enfants.json', 'r+') as file:
        enfants = json.load(file)
        enfants[nom] = enfant
        file.seek(0)
        json.dump(enfants, file, indent=4)

# Exemple d'appel à cette fonction :
# creer_profil("Alice", 100.0, 10.0, "mensuelle", "alicepaypal@example.com", "FR7630006000012345678901234")
