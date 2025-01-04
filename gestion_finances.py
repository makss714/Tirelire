import json
from datetime import datetime

# Fonction pour récupérer la liste des enfants depuis le fichier JSON
def get_enfants():
    try:
        with open('enfants.json', 'r') as file:
            enfants = json.load(file)
    except FileNotFoundError:
        enfants = {}  # Si le fichier n'existe pas encore, retourner un dictionnaire vide
    return enfants

# Fonction pour ajouter un enfant
def ajouter_enfant(enfant):
    enfants = get_enfants()
    enfants[enfant['nom']] = enfant
    with open('enfants.json', 'w') as file:
        json.dump(enfants, file)

# Fonction pour ajouter une somme au solde de l'enfant
def ajouter_solde(nom, montant):
    enfants = get_enfants()
    if nom in enfants:
        enfants[nom]['solde'] += montant
        enfants[nom]['historique'].append({
            'action': 'ajout',
            'montant': montant,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        with open('enfants.json', 'w') as file:
            json.dump(enfants, file)

# Fonction pour retirer une somme du solde de l'enfant
def retirer_solde(nom, montant, mode):
    enfants = get_enfants()
    if nom in enfants and enfants[nom]['solde'] >= montant:
        enfants[nom]['solde'] -= montant
        enfants[nom]['historique'].append({
            'action': 'retrait',
            'montant': montant,
            'mode': mode,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        with open('enfants.json', 'w') as file:
            json.dump(enfants, file)

# Fonction pour récupérer l'historique des transactions d'un enfant
def get_historique(nom):
    enfants = get_enfants()
    if nom in enfants:
        return enfants[nom]['historique']
    return []

# Fonction pour modifier les informations d'un enfant
def modifier_enfant(nom, nouvelles_informations):
    enfants = get_enfants()
    if nom in enfants:
        enfants[nom].update(nouvelles_informations)
        with open('enfants.json', 'w') as file:
            json.dump(enfants, file)
