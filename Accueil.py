import tkinter as tk
from tkinter import simpledialog, messagebox

# Simuler la base de données des enfants avec une liste de dictionnaires
enfants = [
    {"prenom": "Alice", "solde": 100, "argent_poche": 20, "frequence": "hebdomadaire", "paypal": "", "iban": "", "historique": []},
    {"prenom": "Maxence", "solde": 50, "argent_poche": 10, "frequence": "mensuelle", "paypal": "maxence@example.com", "iban": "", "historique": []},
]

class TirelireApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestion de la tirelire des enfants")
        self.master.geometry("500x400")

        # Frame principale
        self.frame_accueil = tk.Frame(self.master)
        self.frame_accueil.pack(pady=20)

        # Boutons des enfants et bouton de création
        self.afficher_boutons_enfants()

    def afficher_boutons_enfants(self):
        """Affiche les boutons pour chaque enfant et le bouton de création."""
        for enfant in enfants:
            bouton = tk.Button(self.frame_accueil, text=enfant["prenom"], command=lambda e=enfant: self.afficher_profil(e))
            bouton.pack(pady=10)

        bouton_creation = tk.Button(self.frame_accueil, text="Créer un nouveau profil", command=self.creer_nouveau_profil)
        bouton_creation.pack(pady=10)

    def afficher_profil(self, enfant):
        """Affiche le profil d'un enfant et ses actions."""
        self.frame_accueil.pack_forget()
        
        # Création du cadre pour le profil de l'enfant
        frame_profil = tk.Frame(self.master)
        frame_profil.pack(pady=20)

        # Informations de l'enfant
        label_prenom = tk.Label(frame_profil, text=f"Profil de {enfant['prenom']}")
        label_prenom.pack()

        label_solde = tk.Label(frame_profil, text=f"Solde: {enfant['solde']}€")
        label_solde.pack()

        # Boutons d'actions
        bouton_ajout = tk.Button(frame_profil, text="AJOUT", command=lambda: self.ajouter_fonds(enfant))
        bouton_ajout.pack(pady=5)

        bouton_retrait = tk.Button(frame_profil, text="RETRAIT", command=lambda: self.retirer_fonds(enfant))
        bouton_retrait.pack(pady=5)

        bouton_historique = tk.Button(frame_profil, text="HISTORIQUE", command=lambda: self.afficher_historique(enfant))
        bouton_historique.pack(pady=5)

        bouton_editer = tk.Button(frame_profil, text="EDITER", command=lambda: self.editer_profil(enfant))
        bouton_editer.pack(pady=5)

        bouton_retour = tk.Button(frame_profil, text="Retour", command=self.retour_accueil)
        bouton_retour.pack(pady=10)

    def ajouter_fonds(self, enfant):
        """Ajoute des fonds au profil de l'enfant."""
        montant_ajout = simpledialog.askfloat("Ajouter des fonds", "Montant à ajouter:")
        if montant_ajout is not None and montant_ajout > 0:
            enfant["solde"] += montant_ajout
            enfant["historique"].append({"type": "crédit", "montant": montant_ajout, "date": "2025-01-04"})
            messagebox.showinfo("Succès", f"{montant_ajout}€ ajoutés au profil de {enfant['prenom']}.")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    def retirer_fonds(self, enfant):
        """Retire des fonds du profil de l'enfant."""
        montant_retrait = simpledialog.askfloat("Retirer des fonds", "Montant à retirer:")
        if montant_retrait is not None and montant_retrait > 0 and montant_retrait <= enfant["solde"]:
            options = []
            if enfant["paypal"]:
                options.append("Paypal")
            if enfant["iban"]:
                options.append("Banque")
            options.append("Cash")
            
            option_retrait = simpledialog.askstring("Choisir méthode de retrait", f"Choisir méthode: {', '.join(options)}")

            if option_retrait == "Cash":
                enfant["solde"] -= montant_retrait
                enfant["historique"].append({"type": "débit", "montant": montant_retrait, "date": "2025-01-04"})
                messagebox.showinfo("Succès", f"{montant_retrait}€ retirés en cash.")
            elif option_retrait == "Paypal" and enfant["paypal"]:
                enfant["solde"] -= montant_retrait
                enfant["historique"].append({"type": "débit", "montant": montant_retrait, "date": "2025-01-04"})
                messagebox.showinfo("Succès", f"{montant_retrait}€ transférés vers Paypal.")
            elif option_retrait == "Banque" and enfant["iban"]:
                enfant["solde"] -= montant_retrait
                enfant["historique"].append({"type": "débit", "montant": montant_retrait, "date": "2025-01-04"})
                messagebox.showinfo("Succès", f"{montant_retrait}€ transférés vers le compte bancaire.")
            else:
                messagebox.showerror("Erreur", "Méthode de retrait non disponible.")
        else:
            messagebox.showerror("Erreur", "Montant invalidé ou insuffisant.")

    def afficher_historique(self, enfant):
        """Affiche l'historique des opérations."""
        historique_window = tk.Toplevel(self.master)
        historique_window.title(f"Historique de {enfant['prenom']}")
        for operation in enfant["historique"]:
            couleur = "green" if operation["type"] == "crédit" else "red"
            label = tk.Label(historique_window, text=f"{operation['date']} - {operation['type']} de {operation['montant']}€", fg=couleur)
            label.pack()

    def editer_profil(self, enfant):
        """Permet d'éditer le profil de l'enfant."""
        self.frame_accueil.pack_forget()
        
        editer_window = tk.Toplevel(self.master)
        editer_window.title(f"Editer le profil de {enfant['prenom']}")

        # Champs pour éditer les informations
        tk.Label(editer_window, text="Prénom:").pack()
        entry_prenom = tk.Entry(editer_window)
        entry_prenom.insert(0, enfant["prenom"])
        entry_prenom.pack()

        tk.Label(editer_window, text="Solde:").pack()
        entry_solde = tk.Entry(editer_window)
        entry_solde.insert(0, str(enfant["solde"]))
        entry_solde.pack()

        tk.Label(editer_window, text="Argent de poche:").pack()
        entry_argent_poche = tk.Entry(editer_window)
        entry_argent_poche.insert(0, str(enfant["argent_poche"]))
        entry_argent_poche.pack()

        tk.Label(editer_window, text="Fréquence:").pack()
        entry_frequence = tk.Entry(editer_window)
        entry_frequence.insert(0, enfant["frequence"])
        entry_frequence.pack()

        tk.Label(editer_window, text="Paypal:").pack()
        entry_paypal = tk.Entry(editer_window)
        entry_paypal.insert(0, enfant["paypal"])
        entry_paypal.pack()

        tk.Label(editer_window, text="IBAN:").pack()
        entry_iban = tk.Entry(editer_window)
        entry_iban.insert(0, enfant["iban"])
        entry_iban.pack()

        def valider_modifications():
            enfant["prenom"] = entry_prenom.get()
            enfant["solde"] = float(entry_solde.get())
            enfant["argent_poche"] = float(entry_argent_poche.get())
            enfant["frequence"] = entry_frequence.get()
            enfant["paypal"] = entry_paypal.get()
            enfant["iban"] = entry_iban.get()
            editer_window.destroy()
            self.afficher_profil(enfant)

        bouton_valider = tk.Button(editer_window, text="Valider", command=valider_modifications)
        bouton_valider.pack(pady=10)

    def creer_nouveau_profil(self):
        """Crée un nouveau profil pour un enfant."""
        fenetre_nouveau = tk.Toplevel(self.master)
        fenetre_nouveau.title("Créer un nouveau profil")

        tk.Label(fenetre_nouveau, text="Prénom:").pack()
        entree_prenom = tk.Entry(fenetre_nouveau)
        entree_prenom.pack()

        tk.Label(fenetre_nouveau, text="Solde:").pack()
        entree_solde = tk.Entry(fenetre_nouveau)
        entree_solde.pack()

        tk.Label(fenetre_nouveau, text="Argent de poche:").pack()
        entree_argent_poche = tk.Entry(fenetre_nouveau)
        entree_argent_poche.pack()

        tk.Label(fenetre_nouveau, text="Fréquence:").pack()
        entree_frequence = tk.Entry(fenetre_nouveau)
        entree_frequence.pack()

        tk.Label(fenetre_nouveau, text="Paypal:").pack()
        entree_paypal = tk.Entry(fenetre_nouveau)
        entree_paypal.pack()

        tk.Label(fenetre_nouveau, text="IBAN:").pack()
        entree_iban = tk.Entry(fenetre_nouveau)
        entree_iban.pack()

        def valider_creation():
            prenom = entree_prenom.get()
            solde = float(entree_solde.get())
            argent_poche = float(entree_argent_poche.get())
            frequence = entree_frequence.get()
            paypal = entree_paypal.get()
            iban = entree_iban.get()

            enfants.append({"prenom": prenom, "solde": solde, "argent_poche": argent_poche, "frequence": frequence,
                            "paypal": paypal, "iban": iban, "historique": []})

            fenetre_nouveau.destroy()
            self.afficher_boutons_enfants()

        bouton_valider = tk.Button(fenetre_nouveau, text="Valider", command=valider_creation)
        bouton_valider.pack(pady=10)

    def retour_accueil(self):
        """Retourne à l'écran d'accueil."""
        self.frame_accueil.pack_forget()
        self.afficher_boutons_enfants()


if __name__ == "__main__":
    root = tk.Tk()
    app = TirelireApp(root)
    root.mainloop()

