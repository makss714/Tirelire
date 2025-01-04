import tkinter as tk
from tkinter import simpledialog, messagebox

class TirelireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Tirelire")

        # Liste des enfants (avec les informations nécessaires pour le retrait)
        self.enfants = [
            {"prenom": "Alice", "solde": 100.0, "argent_poche": 10.0, "frequence": "hebdomadaire", "paypal": "alice@example.com", "iban": "FR7612345678901234567890123", "historique": []},
            {"prenom": "Bob", "solde": 50.0, "argent_poche": 5.0, "frequence": "mensuelle", "paypal": "", "iban": "", "historique": []}
        ]

        self.frame_accueil = tk.Frame(self.root)
        self.frame_accueil.pack(pady=10)
        self.afficher_boutons_enfants()

    def afficher_boutons_enfants(self):
        # Détruire les widgets existants pour éviter les doublons
        for widget in self.frame_accueil.winfo_children():
            widget.destroy()

        # Créer un bouton pour chaque enfant et le lier à son menu
        for enfant in self.enfants:
            bouton = tk.Button(self.frame_accueil, text=f"{enfant['prenom']}", command=lambda e=enfant: self.afficher_menu_enfant(e))
            bouton.pack(pady=5)

        # Ajouter un bouton pour créer un nouvel enfant
        bouton_nouveau = tk.Button(self.frame_accueil, text="Ajouter un enfant", command=self.creer_nouveau_profil)
        bouton_nouveau.pack(pady=5)

    def afficher_menu_enfant(self, enfant):
        # Créer un menu pour chaque enfant
        menu_fenetre = tk.Toplevel(self.root)
        menu_fenetre.title(f"Options pour {enfant['prenom']}")
        
        retrait_button = tk.Button(menu_fenetre, text="Retrait", command=lambda: self.retrait_fonds(enfant))
        retrait_button.pack(pady=10)
        
        historique_button = tk.Button(menu_fenetre, text="Historique", command=lambda: self.afficher_historique(enfant))
        historique_button.pack(pady=10)

        ajouter_button = tk.Button(menu_fenetre, text="Ajouter de l'argent", command=lambda: self.ajouter_argent(enfant))
        ajouter_button.pack(pady=10)

        editer_button = tk.Button(menu_fenetre, text="Editer Profil", command=lambda: self.editer_profil(enfant))
        editer_button.pack(pady=10)

    def retrait_fonds(self, enfant):
        # Créer la fenêtre de retrait
        fenetre_retrait = tk.Toplevel(self.root)
        fenetre_retrait.title("Retrait")

        montant_retrait_label = tk.Label(fenetre_retrait, text="Montant à prélever :")
        montant_retrait_label.pack(pady=5)

        montant_retrait_entry = tk.Entry(fenetre_retrait)
        montant_retrait_entry.pack(pady=5)

        method_label = tk.Label(fenetre_retrait, text="Choisir la méthode de retrait :")
        method_label.pack(pady=5)

        method_var = tk.StringVar(value="Cash")
        method_cash = tk.Radiobutton(fenetre_retrait, text="Cash", variable=method_var, value="Cash")
        method_paypal = tk.Radiobutton(fenetre_retrait, text="PayPal", variable=method_var, value="PayPal")
        method_banque = tk.Radiobutton(fenetre_retrait, text="Banque", variable=method_var, value="Banque")

        method_cash.pack()
        method_paypal.pack()
        method_banque.pack()

        if not enfant["paypal"]:
            method_paypal.config(state=tk.DISABLED)
        if not enfant["iban"]:
            method_banque.config(state=tk.DISABLED)

        def valider_retrait():
            try:
                montant = float(montant_retrait_entry.get())
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
                return

            if montant > enfant["solde"]:
                messagebox.showerror("Erreur", "Le montant dépasse le solde disponible.")
                return

            if method_var.get() == "Cash":
                enfant["solde"] -= montant
                enfant["historique"].append(f"Retrait de {montant}€ en Cash")
            elif method_var.get() == "PayPal" and enfant["paypal"]:
                enfant["solde"] -= montant
                enfant["historique"].append(f"Retrait de {montant}€ vers PayPal ({enfant['paypal']})")
            elif method_var.get() == "Banque" and enfant["iban"]:
                enfant["solde"] -= montant
                enfant["historique"].append(f"Retrait de {montant}€ vers Banque ({enfant['iban']})")
            else:
                messagebox.showerror("Erreur", "Méthode de retrait invalide ou informations manquantes.")
                return

            messagebox.showinfo("Succès", f"Retrait de {montant}€ effectué.")
            fenetre_retrait.destroy()
            self.afficher_boutons_enfants()

    def afficher_historique(self, enfant):
        # Créer la fenêtre d'historique
        fenetre_historique = tk.Toplevel(self.root)
        fenetre_historique.title(f"Historique des opérations de {enfant['prenom']}")

        if not enfant["historique"]:
            messagebox.showinfo("Historique", "Aucune opération enregistrée.")
            return

        for op in enfant["historique"]:
            label = tk.Label(fenetre_historique, text=op, fg="green" if "Retrait de" in op else "red")
            label.pack()

    def editer_profil(self, enfant):
        # Créer la fenêtre d'édition du profil
        fenetre_editer = tk.Toplevel(self.root)
        fenetre_editer.title(f"Editer Profil de {enfant['prenom']}")

        label_prenom = tk.Label(fenetre_editer, text="Prénom :")
        label_prenom.pack(pady=5)
        
        entry_prenom = tk.Entry(fenetre_editer)
        entry_prenom.insert(0, enfant["prenom"])
        entry_prenom.pack(pady=5)

        label_paypal = tk.Label(fenetre_editer, text="PayPal :")
        label_paypal.pack(pady=5)

        entry_paypal = tk.Entry(fenetre_editer)
        entry_paypal.insert(0, enfant["paypal"])
        entry_paypal.pack(pady=5)

        label_iban = tk.Label(fenetre_editer, text="IBAN :")
        label_iban.pack(pady=5)

        entry_iban = tk.Entry(fenetre_editer)
        entry_iban.insert(0, enfant["iban"])
        entry_iban.pack(pady=5)

        def valider_editer():
            enfant["prenom"] = entry_prenom.get()
            enfant["paypal"] = entry_paypal.get()
            enfant["iban"] = entry_iban.get()
            messagebox.showinfo("Succès", "Profil mis à jour avec succès.")
            fenetre_editer.destroy()

        valider_button = tk.Button(fenetre_editer, text="Valider", command=valider_editer)
        valider_button.pack(pady=10)

    def ajouter_argent(self, enfant):
        # Créer la fenêtre pour ajouter de l'argent
        fenetre_ajouter = tk.Toplevel(self.root)
        fenetre_ajouter.title(f"Ajouter de l'argent pour {enfant['prenom']}")

        montant_ajout_label = tk.Label(fenetre_ajouter, text="Montant à ajouter :")
        montant_ajout_label.pack(pady=5)

        montant_ajout_entry = tk.Entry(fenetre_ajouter)
        montant_ajout_entry.pack(pady=5)

        def valider_ajout():
            try:
                montant = float(montant_ajout_entry.get())
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
                return

            enfant["solde"] += montant
            messagebox.showinfo("Succès", f"{montant}€ ajoutés au solde de {enfant['prenom']}.")
            fenetre_ajouter.destroy()

        valider_button = tk.Button(fenetre_ajouter, text="Valider", command=valider_ajout)
        valider_button.pack(pady=10)

    def creer_nouveau_profil(self):
        # Créer la fenêtre pour créer un nouveau profil
        fenetre_nouveau = tk.Toplevel(self.root)
        fenetre_nouveau.title("Créer un nouveau profil")

        label_prenom = tk.Label(fenetre_nouveau, text="Prénom :")
        label_prenom.pack(pady=5)

        entry_prenom = tk.Entry(fenetre_nouveau)
        entry_prenom.pack(pady=5)

        label_montant_depart = tk.Label(fenetre_nouveau, text="Montant de départ :")
        label_montant_depart.pack(pady=5)

        entry_montant_depart = tk.Entry(fenetre_nouveau)
        entry_montant_depart.pack(pady=5)

        label_argent_poche = tk.Label(fenetre_nouveau, text="Montant d'argent de poche :")
        label_argent_poche.pack(pady=5)

        entry_argent_poche = tk.Entry(fenetre_nouveau)
        entry_argent_poche.pack(pady=5)

        label_frequence = tk.Label(fenetre_nouveau, text="Fréquence (hebdomadaire ou mensuelle) :")
        label_frequence.pack(pady=5)

        entry_frequence = tk.Entry(fenetre_nouveau)
        entry_frequence.pack(pady=5)

        label_paypal = tk.Label(fenetre_nouveau, text="PayPal (optionnel) :")
        label_paypal.pack(pady=5)

        entry_paypal = tk.Entry(fenetre_nouveau)
        entry_paypal.pack(pady=5)

        label_iban = tk.Label(fenetre_nouveau, text="IBAN (optionnel) :")
        label_iban.pack(pady=5)

        entry_iban = tk.Entry(fenetre_nouveau)
        entry_iban.pack(pady=5)

        def valider_creation():
            prenom = entry_prenom.get()
            try:
                montant_depart = float(entry_montant_depart.get())
                argent_poche = float(entry_argent_poche.get())
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des montants valides.")
                return

            frequence = entry_frequence.get()
            paypal = entry_paypal.get()
            iban = entry_iban.get()

            # Ajouter l'enfant à la liste des enfants
            self.enfants.append({"prenom": prenom, "solde": montant_depart, "argent_poche": argent_poche, "frequence": frequence, "paypal": paypal, "iban": iban, "historique": []})
            messagebox.showinfo("Succès", f"Profil de {prenom} créé avec succès.")
            fenetre_nouveau.destroy()
            self.afficher_boutons_enfants()

        valider_button = tk.Button(fenetre_nouveau, text="Valider", command=valider_creation)
        valider_button.pack(pady=10)

# Création de la fenêtre principale
root = tk.Tk()
app = TirelireApp(root)
root.mainloop()



