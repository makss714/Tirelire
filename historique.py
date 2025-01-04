from gestion_finances import get_historique

def afficher_historique(nom):
    historique = get_historique(nom)
    if not historique:
        print(f"Aucun historique pour {nom}.")
        return

    for operation in historique:
        couleur = 'green' if operation['action'] == 'ajout' else 'red'
        print(f"{operation['date']} - {operation['action']} : {operation['montant']}€ (Mode: {operation.get('mode', 'N/A')})")
        print(f"Code couleur: {couleur}")
