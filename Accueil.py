import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import datetime

# Classe représentant un enfant
class Enfant:
    def __init__(self, prenom, solde_initial, argent_poche, frequence, paypal=None, iban=None):
        self.prenom = prenom
        self.solde = solde_initial
        self.argent_poche = argent_poche
        self.frequence = frequence
        self.paypal = paypal
        self.iban = iban
        self.historique = []  # Historique des opérations
    
    def ajouter_fonds(self, montant):
        self.solde += montant
        self.historique.append({"type": "crédit", "montant": montant, "date": datetime.datetime.now()})
    
    def retirer_fonds(self, montant, mode):
        if self.solde >= montant:
            self.solde -= montant
            self.historique.append({"type": "débit", "montant": montant, "mode": mode, "date": datetime.datetime.now()})
        else:
            messagebox.showerror("Erreur", "Fonds insuffisants pour le retrait.")
    
    def afficher_historique(self):
        historique_str = ""
        for operation in self.historique:
            type_op = "Crédit" if operation["type"] == "crédit" else "Débit"
            montant = operation["montant"]
            date = operation["date"].strftime("%Y-%m-%d %H:%M:%S")
            mode = operation.get("mode", "")
            historique_str += f"{type_op} - Montant: {montant} € - Date: {date} {f'- Mode: {mode}' if mode else ''}\n"
        return historique_str

    def editer_profil(self, prenom=None, solde=None, argent_poche=None, frequence=None, paypal=None, iban=None):
        if prenom: self.prenom = prenom
        if solde is not None: self.solde = solde
        if argent_poche is not None: self.argent_poche = argent_poche
        if frequence: self.frequence = frequence
        if paypal: self.paypal = paypal
        if iban: self.iban = iban

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion de la tirelire des enfants")
root.geometry("600x500")

# Liste pour stocker les profils des enfants
enfants = []

# Fonction pour afficher l'écran de création d'un enfant
def creer_profil():
    def valider_profil():
        prenom = entry_prenom.get()
        montant_initial = float(entry_montant_initial.get())
        argent_poche = float(entry_argent_poche.get())
        frequence = frequence_var.get()
        paypal = entry_paypal.get() if entry_paypal.get() else None
        iban = entry_iban.get() if entry_iban.get() else None

        # Créer l'enfant et ajouter à la liste
        enfant = Enfant(prenom, montant_initial, argent_poche, frequence, paypal, iban)
        enfants.append(enfant)
        messagebox.showinfo("Succès", f"Profil de {prenom} créé avec succès !")
        fenetre_creation.destroy()
        afficher_accueil()

    # Fenêtre de création d'enfant
    fenetre_creation = tk.Toplevel(root)
    fenetre_creation.title("Créer un Profil Enfant")
    fenetre_creation.geometry("450x500")
    
    # Labels et champs de saisie
    tk.Label(fenetre_creation, text="Prénom de l'enfant:").pack()
    entry_prenom = tk.Entry(fenetre_creation)
    entry_prenom.pack()

    tk.Label(fenetre_creation, text="Montant initial:").pack()
    entry_montant_initial = tk.Entry(fenetre_creation)
    entry_montant_initial.pack()

    tk.Label(fenetre_creation, text="Montant d'argent de poche:").pack()
    entry_argent_poche = tk.Entry(fenetre_creation)
    entry_argent_poche.pack()

    tk.Label(fenetre_creation, text="Fréquence (hebdomadaire / mensuelle):").pack()
    frequence_var = tk.StringVar(value="hebdomadaire")
    tk.Radiobutton(fenetre_creation, text="Hebdomadaire", variable=frequence_var, value="hebdomadaire").pack()
    tk.Radiobutton(fenetre_creation, text="Mensuelle", variable=frequence_var, value="mensuelle").pack()

    tk.Label(fenetre_creation, text="Compte Paypal (optionnel):").pack()
    entry_paypal = tk.Entry(fenetre_creation)
    entry_paypal.pack()

    tk.Label(fenetre_creation, text="IBAN (optionnel):").pack()
    entry_iban = tk.Entry(fenetre_creation)
    entry_iban.pack()

    # Bouton pour valider le profil
    tk.Button(fenetre_creation, text="Valider", command=valider_profil).pack()

# Fonction pour afficher le profil d'un enfant
def afficher_profil(enfant):
    def ajouter_fonds():
        montant = float(simpledialog.askstring("Ajouter des fonds", "Montant à ajouter:"))
        enfant.ajouter_fonds(montant)
        messagebox.showinfo("Succès", f"Montant ajouté : {montant} €")
    
    def retirer_fonds():
        montant = float(simpledialog.askstring("Retirer des fonds", "Montant à retirer:"))
        mode = simpledialog.askstring("Mode de retrait", "Choisissez entre Cash, Paypal ou Banque:")
        if mode not in ['Cash', 'Paypal', 'Banque'] or (mode in ['Paypal', 'Banque'] and not (enfant.paypal or enfant.iban)):
            messagebox.showerror("Erreur", "Mode de retrait invalide.")
            return
        enfant.retirer_fonds(montant, mode)
        messagebox.showinfo("Succès", f"Montant retiré : {montant} € via {mode}")
    
    def afficher_historique():
        historique = enfant.afficher_historique()
        messagebox.showinfo("Historique", historique)
    
    def editer_profil():
        def valider_edition():
            prenom = entry_prenom.get()
            solde = float(entry_solde.get())
            argent_poche = float(entry_argent_poche.get())
            frequence = frequence_var.get()
            paypal = entry_paypal.get() if entry_paypal.get() else None
            iban = entry_iban.get() if entry_iban.get() else None

            enfant.editer_profil(prenom, solde, argent_poche, frequence, paypal, iban)
            messagebox.showinfo("Succès", "Profil mis à jour avec succès.")
            fenetre_edition.destroy()
            afficher_profil(enfant)

        fenetre_edition = tk.Toplevel(root)
        fenetre_edition.title("Édition du Profil")
        fenetre_edition.geometry("400x400")
        
        # Labels et champs de saisie
        tk.Label(fenetre_edition, text="Prénom de l'enfant:").pack()
        entry_prenom = tk.Entry(fenetre_edition)
        entry_prenom.insert(0, enfant.prenom)
        entry_prenom.pack()

        tk.Label(fenetre_edition, text="Solde actuel:").pack()
        entry_solde = tk.Entry(fenetre_edition)
        entry_solde.insert(0, str(enfant.solde))
        entry_solde.pack()

        tk.Label(fenetre_edition, text="Montant d'argent de poche:").pack()
        entry_argent_poche = tk.Entry(fenetre_edition)
        entry_argent_poche.insert(0, str(enfant.argent_poche))
        entry_argent_poche.pack()

        tk.Label(fenetre_edition, text="Fréquence (hebdomadaire / mensuelle):").pack()
        frequence_var = tk.StringVar(value=enfant.frequence)
        tk.Radiobutton(fenetre_edition, text="Hebdomadaire", variable=frequence_var, value="hebdomadaire").pack()
        tk.Radiobutton(fenetre_edition, text="Mensuelle", variable=frequence_var, value="mensuelle").pack()

        tk.Label(fenetre_edition, text="Compte Paypal (optionnel):").pack()
        entry_paypal = tk.Entry(fenetre_edition)
        entry_paypal.insert(0, enfant.paypal if enfant.paypal else "")
        entry_paypal.pack()

        tk.Label(fenetre_edition, text="IBAN (optionnel):").pack()
        entry_iban = tk.Entry(fenetre_edition)
        entry_iban.insert(0, enfant.iban if enfant.iban else "")
        entry_iban.pack()

        # Bouton pour valider les modifications
        tk.Button(fenetre_edition, text="Valider", command=valider_edition).pack()

    # Fenêtre de profil de l'enfant
    fenetre_profil = tk.Toplevel(root)
    fenetre_profil.title(f"Profil de {enfant.prenom}")
    fenetre_profil.geometry("500x500")
    
    # Affichage du solde
    tk.Label(fenetre_profil, text=f"Solde actuel : {enfant.solde} €").pack()
    
    # Boutons
    tk.Button(fenetre_profil, text="Ajouter des fonds", command=ajouter_fonds).pack()
    tk.Button(fenetre_profil, text="Retirer des fonds", command=retirer_fonds).pack()
    tk.Button(fenetre_profil, text="Afficher l'historique", command=afficher_historique).pack()
    tk.Button(fenetre_profil, text="Éditer le profil", command=editer_profil).pack()

# Fonction pour afficher l'accueil
def afficher_accueil():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bienvenue dans la gestion de tirelire", font=("Arial", 16)).pack()

    for enfant in enfants:
        bouton_profil = tk.Button(root, text=f"{enfant.prenom}", command=lambda e=enfant: afficher_profil(e))
        bouton_profil.pack(pady=5)

    tk.Button(root, text="Créer un profil", command=creer_profil).pack(pady=10)

# Lancer l'application
afficher_accueil()
root.mainloop()







