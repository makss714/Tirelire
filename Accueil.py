import tkinter as tk
import json

class TirelireApp:
    def __init__(self, root):
        self.root = root
        self.enfants = self.charger_enfants()  # Charger les données depuis le fichier enfants.json
        self.setup_ui()

    def charger_enfants(self):
        """Charge les données des enfants depuis le fichier JSON."""
        with open('enfants.json', 'r') as file:
            return json.load(file)

    def setup_ui(self):
        """Configure l'interface graphique de l'application."""
        self.frame_accueil = tk.Frame(self.root)
        self.frame_accueil.pack()

        # Création des boutons pour chaque enfant
        for i, enfant in enumerate(self.enfants):
            if isinstance(enfant, dict):  # Vérification que 'enfant' est un dictionnaire
                bouton = tk.Button(self.frame_accueil, text=enfant["prenom"], command=lambda i=i: self.afficher_profil(i))
                bouton.pack()
            else:
                print(f"Erreur : L'élément à l'index {i} n'est pas un dictionnaire.")

        # Ajouter un bouton pour créer un nouveau profil enfant
        bouton_nouveau_profil = tk.Button(self.frame_accueil, text="Créer un nouveau profil", command=self.creer_nouveau_profil)
        bouton_nouveau_profil.pack()

    def afficher_profil(self, i):
        """Affiche le profil de l'enfant sélectionné."""
        enfant = self.enfants[i]
        print(f"Affichage du profil de l'enfant: {enfant['prenom']}")

        # Créer une nouvelle fenêtre pour afficher le profil détaillé
        fenetre_profil = tk.Toplevel(self.root)
        fenetre_profil.title(f"Profil de {enfant['prenom']}")

        # Afficher le solde de l'enfant
        label_solde = tk.Label(fenetre_profil, text=f"Solde: {enfant['solde']}€")
        label_solde.pack()

        # Ajouter des boutons pour AJOUT, RETRAIT, HISTORIQUE et EDITER
        bouton_ajout = tk.Button(fenetre_profil, text="AJOUT", command=lambda: self.ajouter_fonds(i))
        bouton_ajout.pack()

        bouton_retrait = tk.Button(fenetre_profil, text="RETRAIT", command=lambda: self.retirer_fonds(i))
        bouton_retrait.pack()

        bouton_historique = tk.Button(fenetre_profil, text="HISTORIQUE", command=lambda: self.afficher_historique(i))
        bouton_historique.pack()

        bouton_editer = tk.Button(fenetre_profil, text="EDITER", command=lambda: self.editer_profil(i))
        bouton_editer.pack()

    def ajouter_fonds(self, i):
        """Ajoute des fonds au solde de l'enfant."""
        enfant = self.enfants[i]
        montant_ajouter = tk.simpledialog.askfloat("Ajouter des fonds", "Montant à ajouter:")
        if montant_ajouter and montant_ajouter > 0:
            enfant['solde'] += montant_ajouter
            print(f"Montant ajouté: {montant_ajouter}€. Nouveau solde: {enfant['solde']}€")
            self.enfants[i] = enfant  # Mettre à jour la liste d'enfants

    def retirer_fonds(self, i):
        """Retire des fonds du solde de l'enfant."""
        enfant = self.enfants[i]
        montant_retrait = tk.simpledialog.askfloat("Retirer des fonds", "Montant à retirer:")
        if montant_retrait and montant_retrait > 0 and enfant['solde'] >= montant_retrait:
            enfant['solde'] -= montant_retrait
            print(f"Montant retiré: {montant_retrait}€. Nouveau solde: {enfant['solde']}€")
            self.enfants[i] = enfant  # Mettre à jour la liste d'enfants

    def afficher_historique(self, i):
        """Affiche l'historique des transactions de l'enfant."""
        enfant = self.enfants[i]
        print(f"Historique des transactions de {enfant['prenom']}:")
        # Affichage de l'historique des opérations (exemple fictif)
        for operation in enfant.get("historique", []):
            print(f"{operation['type']} de {operation['montant']}€ le {operation['date']}")

    def editer_profil(self, i):
        """Permet d'éditer le profil de l'enfant."""
        enfant = self.enfants[i]
        print(f"Modification du profil de {enfant['prenom']}")

        # Créer une fenêtre d'édition
        fenetre_editer = tk.Toplevel(self.root)
        fenetre_editer.title(f"Modifier le profil de {enfant['prenom']}")

        # Champ pour le prénom
        label_prenom = tk.Label(fenetre_editer, text="Prénom:")
        label_prenom.pack()
        entree_prenom = tk.Entry(fenetre_editer)
        entree_prenom.insert(0, enfant["prenom"])
        entree_prenom.pack()

        # Champ pour le solde
        label_solde = tk.Label(fenetre_editer, text="Solde:")
        label_solde.pack()
        entree_solde = tk.Entry(fenetre_editer)
        entree_solde.insert(0, str(enfant["solde"]))
        entree_solde.pack()

        # Bouton pour valider l'édition
        bouton_valider = tk.Button(fenetre_editer, text="Valider", command=lambda: self.valider_modifications(i, entree_prenom.get(), entree_solde.get()))
        bouton_valider.pack()

    def valider_modifications(self, i, nouveau_prenom, nouveau_solde):
        """Valide les modifications du profil de l'enfant."""
        enfant = self.enfants[i]
        enfant['prenom'] = nouveau_prenom
        enfant['solde'] = float(nouveau_solde)
        self.enfants[i] = enfant  # Mettre à jour la liste des enfants
        print(f"Profil modifié pour {nouveau_prenom} avec un solde de {nouveau_solde}€.")

    def creer_nouveau_profil(self):
        """Crée un nouveau profil enfant."""
        print("Création d'un nouveau profil enfant")

        # Créer une fenêtre pour entrer les informations du nouvel enfant
        fenetre_nouveau = tk.Toplevel(self.root)
        fenetre_nouveau.title("Créer un nouveau profil")

        # Champs pour les informations de l'enfant
        label_prenom = tk.Label(fenetre_nouveau, text="Prénom:")
        label_prenom.pack()
        entree_prenom = tk.Entry(fenetre_nouveau)
        entree_prenom.pack()

        label_solde = tk.Label(fenetre_nouveau, text="Montant de départ:")
        label_solde.pack()
        entree_solde = tk.Entry(fenetre_nouveau)
        entree_solde.pack()

        label_argent_poche = tk.Label(fenetre_nouveau, text="Montant de l'argent de poche:")
        label_argent_poche.pack()
        entree_argent_poche = tk.Entry(fenetre_nouveau)
        entree_argent_poche.pack()

        label_frequence = tk.Label(fenetre_nouveau, text="Fréquence (hebdomadaire/mensuelle):")
        label_frequence.pack()
        entree_frequence = tk.Entry(fenetre_nouveau)
        entree_frequence.pack()

        bouton_valider = tk.Button(fenetre_nouveau, text="Valider", command=lambda: self.valider_creation_nouveau_profil(entree_prenom.get(), entree_solde.get(), entree_argent_poche.get(), entree_frequence.get()))
        bouton_valider.pack()

    def valider_creation_nouveau_profil(self, prenom, solde, argent_poche, frequence):
        """Valide la création du nouveau profil."""
        # Créer un nouvel enfant avec les données saisies
        nouvel_enfant = {
            "prenom": prenom,
            "solde": float(solde),
            "argent_de_poche": float(argent_poche),
            "frequence": frequence
        }
        self.enfants.append(nouvel_enfant)  # Ajouter le nouvel enfant à la liste
        print(f"Profil de {prenom} créé avec un solde de {solde}€.")

# Code principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TirelireApp(root)
    root.mainloop()

