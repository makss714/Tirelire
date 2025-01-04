import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class TirelireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de la Tirelire")
        self.root.geometry("600x400")

        # Charger les profils d'enfants depuis le fichier JSON
        self.enfants = self.charger_enfants()

        # Création de la frame principale
        self.frame_accueil = tk.Frame(self.root)
        self.frame_accueil.pack(fill="both", expand=True)

        # Bouton pour créer un nouveau profil
        self.bouton_creation = tk.Button(self.frame_accueil, text="Créer un nouveau profil", command=self.creer_profil)
        self.bouton_creation.pack(pady=10)

        # Afficher les boutons pour chaque enfant existant
        self.afficher_boutons_enfants()

    def charger_enfants(self):
        """Charge les profils d'enfants à partir du fichier JSON"""
        try:
            with open("enfants.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Retourne une liste vide si le fichier n'existe pas

    def sauvegarder_enfants(self):
        """Sauvegarde les profils des enfants dans un fichier JSON"""
        with open("enfants.json", "w") as file:
            json.dump(self.enfants, file, indent=4)

    def afficher_boutons_enfants(self):
        """Affiche un bouton pour chaque enfant dans le profil"""
        # D'abord, on nettoie le frame de l'interface pour éviter les doublons de boutons
        for widget in self.frame_accueil.winfo_children():
            if widget != self.bouton_creation:  # Conserver le bouton de création
                widget.destroy()  # Efface les anciens widgets

        # Afficher de nouveau le bouton de création
        self.bouton_creation.pack(pady=10)

        # Afficher les boutons des enfants
        for i, enfant in enumerate(self.enfants):
            bouton = tk.Button(self.frame_accueil, text=enfant["prenom"], command=lambda i=i: self.afficher_profil(i))
            bouton.pack(pady=5)

    def creer_profil(self):
        """Affiche un formulaire pour créer un nouveau profil enfant"""
        fenetre_nouveau = tk.Toplevel(self.root)
        fenetre_nouveau.title("Créer un nouveau profil")

        tk.Label(fenetre_nouveau, text="Prénom de l'enfant:").pack(pady=5)
        entree_prenom = tk.Entry(fenetre_nouveau)
        entree_prenom.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Montant de départ:").pack(pady=5)
        entree_solde = tk.Entry(fenetre_nouveau)
        entree_solde.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Montant d'argent de poche:").pack(pady=5)
        entree_argent_poche = tk.Entry(fenetre_nouveau)
        entree_argent_poche.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Fréquence (hebdomadaire/mensuelle):").pack(pady=5)
        entree_frequence = tk.Entry(fenetre_nouveau)
        entree_frequence.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Compte Paypal (optionnel):").pack(pady=5)
        entree_paypal = tk.Entry(fenetre_nouveau)
        entree_paypal.pack(pady=5)

        tk.Label(fenetre_nouveau, text="IBAN (optionnel):").pack(pady=5)
        entree_iban = tk.Entry(fenetre_nouveau)
        entree_iban.pack(pady=5)

        def valider_creation_nouveau_profil():
            """Valide la création d'un nouveau profil"""
            prenom = entree_prenom.get()
            solde = entree_solde.get()
            argent_poche = entree_argent_poche.get()
            frequence = entree_frequence.get()
            paypal = entree_paypal.get()
            iban = entree_iban.get()

            if not prenom or not solde or not argent_poche or not frequence:
                messagebox.showerror("Erreur", "Tous les champs obligatoires doivent être remplis.")
                return

            try:
                solde = float(solde)
                argent_poche = float(argent_poche)
            except ValueError:
                messagebox.showerror("Erreur", "Le montant de départ et d'argent de poche doivent être des nombres.")
                return

            enfant = {
                "prenom": prenom,
                "solde": solde,
                "argent_poche": argent_poche,
                "frequence": frequence,
                "paypal": paypal if paypal else None,
                "iban": iban if iban else None,
                "historique": []
            }

            self.enfants.append(enfant)
            self.sauvegarder_enfants()
            self.afficher_boutons_enfants()
            fenetre_nouveau.destroy()

        bouton_valider = tk.Button(fenetre_nouveau, text="Valider", command=valider_creation_nouveau_profil)
        bouton_valider.pack(pady=10)

    def afficher_profil(self, index):
        """Affiche les informations d'un enfant et propose des actions"""
        enfant = self.enfants[index]
        fenetre_profil = tk.Toplevel(self.root)
        fenetre_profil.title(f"Profil de {enfant['prenom']}")

        tk.Label(fenetre_profil, text=f"Prénom: {enfant['prenom']}").pack(pady=5)
        tk.Label(fenetre_profil, text=f"Solde: {enfant['solde']}€").pack(pady=5)
        tk.Label(fenetre_profil, text=f"Argent de poche: {enfant['argent_poche']}€").pack(pady=5)
        tk.Label(fenetre_profil, text=f"Fréquence: {enfant['frequence']}").pack(pady=5)

        bouton_ajout = tk.Button(fenetre_profil, text="AJOUT", command=lambda: self.ajouter_fonds(index))
        bouton_ajout.pack(pady=5)

        bouton_retrait = tk.Button(fenetre_profil, text="RETRAIT", command=lambda: self.retirer_fonds(index))
        bouton_retrait.pack(pady=5)

        bouton_historique = tk.Button(fenetre_profil, text="HISTORIQUE", command=lambda: self.afficher_historique(index))
        bouton_historique.pack(pady=5)

        bouton_modifier = tk.Button(fenetre_profil, text="EDITER", command=lambda: self.modifier_profil(index))
        bouton_modifier.pack(pady=5)

    def ajouter_fonds(self, index):
        """Permet d'ajouter des fonds au profil d'un enfant"""
        montant_ajout = simpledialog.askfloat("Ajouter des fonds", "Montant à ajouter:")
        if montant_ajout and montant_ajout > 0:
            self.enfants[index]["solde"] += montant_ajout
            self.enfants[index]["historique"].append(f"Ajout de {montant_ajout}€")
            self.sauvegarder_enfants()

    def retirer_fonds(self, index):
        """Permet de retirer des fonds du profil d'un enfant"""
        montant_retrait = simpledialog.askfloat("Retirer des fonds", "Montant à retirer:")
        if montant_retrait and montant_retrait > 0 and self.enfants[index]["solde"] >= montant_retrait:
            self.enfants[index]["solde"] -= montant_retrait
            self.enfants[index]["historique"].append(f"Retrait de {montant_retrait}€")
            self.sauvegarder_enfants()
        else:
            messagebox.showerror("Erreur", "Montant invalide ou solde insuffisant.")

    def afficher_historique(self, index):
        """Affiche l'historique des transactions de l'enfant"""
        enfant = self.enfants[index]
        fenetre_historique = tk.Toplevel(self.root)
        fenetre_historique.title(f"Historique de {enfant['prenom']}")

        for transaction in enfant["historique"]:
            label = tk.Label(fenetre_historique, text=transaction)
            label.pack(pady=2)

    def modifier_profil(self, index):
        """Permet de modifier les informations d'un enfant"""
        enfant = self.enfants[index]
        fenetre_modifier = tk.Toplevel(self.root)
        fenetre_modifier.title(f"Modifier le profil de {enfant['prenom']}")

        # Ajouter les champs à modifier ici...
        # Utilisez les mêmes champs que pour la création mais remplis avec les valeurs actuelles
        # Puis, appliquez la modification en sauvegardant les nouvelles valeurs dans l'objet enfant

def run():
    root = tk.Tk()
    app = TirelireApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()


