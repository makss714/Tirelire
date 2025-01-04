from gestion_finances import modifier_enfant

def modifier_profil(nom, nouvelles_informations):
    modifier_enfant(nom, nouvelles_informations)

# Exemple d'utilisation :
# modifier_profil("Alice", {"solde": 150.0, "paypal": "alicepaypal_new@example.com"})
