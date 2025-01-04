import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Création de la classe pour l'interface graphique
class TirelireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de la Tirelire")

        self.listePersonne = self.charger_donnees()
        self.setup_ui()

    def setup_ui(self):
        # Page d'accueil
        self.frame_accueil = tk.Frame(self.root)
        self.frame_accueil.pack(fill="both", expand=True)

        # Affichage des boutons pour chaque enfant
        for i, enfant in enumerate(self.listePersonne):
            bouton = tk.Button(self.frame_accueil, text=enfant["prenom"], command=lambda i=i: self.afficher_profil(i))
            bouton.pack(pady=10)

        # Bouton pour ajouter un nouvel enfant
        bouton_ajouter = tk.Button(self.frame_accueil, text="Créer un Profil", command=self.creer_profil)
        bouton_ajouter.pack(pady=20)

    def charger_donnees(self):
        # Charger les données des enfants depuis un fichier JSON
        if os.path.exists("enfants.json"):
            with open("enfants.json", "r") as file:
                return json.load(file)
        return []

    def enregistrer_donnees(self):
        # Enregistrer les données des enfants dans un fichier JSON
        with open("enfants.json", "w") as file:
            json.dump(self.listePersonne, file)

    def creer_profil(self):
        # Ouvrir une fenêtre pour créer un nouveau profil enfant
        self.frame_accueil.pack_forget()

        self.frame_creation = tk.Frame(self.root)
        self.frame_creation.pack(fill="both", expand=True)

        tk.Label(self.frame_creation, text="Prénom de l'enfant:").pack()
        self.prenom_entry = tk.Entry(self.frame_creation)
        self.prenom_entry.pack(pady=10)

        tk.Label(self.frame_creation, text="Montant de départ:").pack()
        self.montant_entry = tk.Entry(self.frame_creation)
        self.montant_entry.pack(pady=10)

        tk.Label(self.frame_creation, text="Argent de poche hebdomadaire:").pack()
        self.argent_poche_entry = tk.Entry(self.frame_creation)
        self.argent_poche_entry.pack(pady=10)

        tk.Label(self.frame_creation, text="Fréquence (hebdomadaire/mensuelle):").pack()
        self.frequence_entry = tk.Entry(self.frame_creation)
        self.frequence_entry.pack(pady=10)

        tk.Label(self.frame_creation, text="Compte PayPal (optionnel):").pack()
        self.paypal_entry = tk.Entry(self.frame_creation)
        self.paypal_entry.pack(pady=10)

        tk.Label(self.frame_creation, text="IBAN (optionnel):").pack()
        self.iban_entry = tk.Entry(self.frame_creation)
        self.iban_entry.pack(pady=10)

        bouton_valider = tk.Button(self.frame_creation, text="Valider", command=self.valider_creation)
        bouton_valider.pack(pady=20)

    def valider_creation(self):
        # Valider la création du profil
        prenom = self.prenom_entry.get()
        montant = self.montant_entry.get()
        argent_poche = self.argent_poche_entry.get()
        frequence = self.frequence_entry.get()
        paypal = self.paypal_entry.get()
        iban = self.iban_entry.get()

        # Vérification des champs
        if not prenom or not montant or not argent_poche or not frequence:
            messagebox.showerror("Erreur", "Tous les champs obligatoires doivent être remplis")
            return

        enfant = {
            "prenom": prenom,
            "montant": float(montant),
            "argent_poche": float(argent_poche),
            "frequence": frequence,
            "paypal": paypal,
            "iban": iban,
            "historique": []
        }

        self.listePersonne.append(enfant)
        self.enregistrer_donnees()

        # Retour à la page d'accueil
        self.frame_creation.pack_forget()
        self.setup_ui()

    def afficher_profil(self, index):
        # Afficher les détails d'un enfant
        self.frame_accueil.pack_forget()

        enfant = self.listePersonne[index]
        self.frame_profil = tk.Frame(self.root)
        self.frame_profil.pack(fill="both", expand=True)

        tk.Label(self.frame_profil, text=f"Solde de {enfant['prenom']}: {enfant['montant']}€").pack(pady=10)

        bouton_ajouter = tk.Button(self.frame_profil, text="AJOUT", command=lambda: self.ajout_fonds(index))
        bouton_ajouter.pack(pady=5)

        bouton_retrait = tk.Button(self.frame_profil, text="RETRAIT", command=lambda: self.retrait_fonds(index))
        bouton_retrait.pack(pady=5)

        bouton_historique = tk.Button(self.frame_profil, text="HISTORIQUE", command=lambda: self.afficher_historique(index))
        bouton_historique.pack(pady=5)

        bouton_modifier = tk.Button(self.frame_profil, text="EDITER", command=lambda: self.modifier_profil(index))
        bouton_modifier.pack(pady=5)

    def ajout_fonds(self, index):
        # Ajouter des fonds au profil
        self.frame_profil.pack_forget()
        self.frame_ajout = tk.Frame(self.root)
        self.frame_ajout.pack(fill="both", expand=True)

        tk.Label(self.frame_ajout, text="Montant à ajouter:").pack()
        self.montant_ajout_entry = tk.Entry(self.frame_ajout)
        self.montant_ajout_entry.pack(pady=10)

        bouton_valider = tk.Button(self.frame_ajout, text="Valider", command=lambda: self.valider_ajout(index))
        bouton_valider.pack(pady=20)

    def valider_ajout(self, index):
        montant_ajouter = self.montant_ajout_entry.get()
        if not montant_ajouter:
            messagebox.showerror("Erreur", "Veuillez entrer un montant à ajouter")
            return

        enfant = self.listePersonne[index]
        enfant["montant"] += float(montant_ajouter)
        enfant["historique"].append({"operation": "Ajout", "montant": float(montant_ajouter), "date": "Aujourd'hui", "type": "credit"})

        self.enregistrer_donnees()
        self.frame_ajout.pack_forget()
        self.afficher_profil(index)

    def retrait_fonds(self, index):
        # Retirer des fonds du profil
        self.frame_profil.pack_forget()
        self.frame_retrait = tk.Frame(self.root)
        self.frame_retrait.pack(fill="both", expand=True)

        tk.Label(self.frame_retrait, text="Montant à prélever:").pack()
        self.montant_retrait_entry = tk.Entry(self.frame_retrait)
        self.montant_retrait_entry.pack(pady=10)

        tk.Label(self.frame_retrait, text="Méthode de paiement:").pack()
        self.methode_retrait = ttk.Combobox(self.frame_retrait, values=["Cash", "Paypal", "Banque"])
        self.methode_retrait.pack(pady=10)

        bouton_valider = tk.Button(self.frame_retrait, text="Valider", command=lambda: self.valider_retrait(index))
        bouton_valider.pack(pady=20)

    def valider_retrait(self, index):
        montant_retrait = self.montant_retrait_entry.get()
        methode = self.methode_retrait.get()
        if not montant_retrait or not methode:
            messagebox.showerror("Erreur", "Veuillez entrer un montant et une méthode de paiement")
            return

        enfant = self.listePersonne[index]
        enfant["montant"] -= float(montant_retrait)
        enfant["historique"].append({"operation": "Retrait", "montant": float(montant_retrait), "date": "Aujourd'hui", "type": "debit"})

        self.enregistrer_donnees()
        self.frame_retrait.pack_forget()
        self.afficher_profil(index)

    def afficher_historique(self, index):
        # Afficher l'historique des opérations
        self.frame_profil.pack_forget()
        self.frame_historique = tk.Frame(self.root)
        self.frame_historique.pack(fill="both", expand=True)

        enfant = self.listePersonne[index]
        for operation in enfant["historique"]:
            couleur = "green" if operation["type"] == "credit" else "red"
            label = tk.Label(self.frame_historique, text=f"{operation['operation']} : {operation['montant']}€ le {operation['date']}", fg=couleur)
            label.pack(pady=5)

        bouton_retour = tk.Button(self.frame_historique, text="Retour", command=lambda: self.afficher_profil(index))
        bouton_retour.pack(pady=20)

    def modifier_profil(self, index):
        # Modifier les informations du profil
        self.frame_profil.pack_forget()
        self.creer_profil()  # Ouverture du formulaire pour modification avec les anciennes informations

if __name__ == "__main__":
    root = tk.Tk()
    app = TirelireApp(root)
    root.mainloop()
