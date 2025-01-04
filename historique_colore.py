from gestion_finances import get_historique

def afficher_historique_colore(nom):
    historique = get_historique(nom)
    if not historique:
        print(f"Aucun historique pour {nom}.")
        return

    for operation in historique:
        couleur = 'green' if operation['action'] == 'ajout' else 'red'
        print(f"\033[1;32m{operation['date']} - {operation['action']} : {operation['montant']}€ (Mode: {operation.get('mode', 'N/A')})\033[0m")
        print(f"Code couleur: {couleur}")

# Exemple d'appel :
# afficher_historique_colore("John Doe")
