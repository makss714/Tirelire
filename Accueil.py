import tkinter as tk
import tkinter.simpledialog as simpledialog

class Application:
    def __init__(self):
        self.profils = []  # Liste pour stocker les profils enfants
        self.fenetre = tk.Tk()
        self.fenetre.title("Gestion de Tirelire")

        self.frame_accueil = tk.Frame(self.fenetre)
        self.frame_accueil.pack(padx=10, pady=10)

        self.afficher_profils()

        self.fenetre.mainloop()

    def afficher_profils(self):
        """Met à jour l'affichage des profils"""
        # Vider la liste actuelle des profils affichés
        for item in self.frame_accueil.winfo_children():
            item.destroy()

        # Ajouter un bouton pour chaque profil existant
        for i, enfant in enumerate(self.profils):
            bouton = tk.Button(self.frame_accueil, text=enfant["prenom"], command=lambda i=i: self.afficher_profil(i))
            bouton.pack(pady=5)

        # Ajouter un bouton pour créer un nouveau profil
        bouton_nouveau = tk.Button(self.frame_accueil, text="Créer un nouveau profil", command=self.creer_nouveau_profil)
        bouton_nouveau.pack(pady=10)

    def creer_nouveau_profil(self):
        """Créer un nouveau profil enfant"""
        fenetre_nouveau = tk.Toplevel()
        fenetre_nouveau.title("Création d'un nouveau profil")

        tk.Label(fenetre_nouveau, text="Prénom:").pack(pady=5)
        entree_prenom = tk.Entry(fenetre_nouveau)
        entree_prenom.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Solde:").pack(pady=5)
        entree_solde = tk.Entry(fenetre_nouveau)
        entree_solde.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Argent de poche:").pack(pady=5)
        entree_argent_poche = tk.Entry(fenetre_nouveau)
        entree_argent_poche.pack(pady=5)

        tk.Label(fenetre_nouveau, text="Fréquence (hebdomadaire/mensuelle):").pack(pady=5)
        entree_frequence = tk.Entry(fenetre_nouveau)
        entree_frequence.pack(pady=5)

        bouton_valider = tk.Button(fenetre_nouveau, text="Valider", command=lambda: self.valider_creation_nouveau_profil(entree_prenom.get(), entree_solde.get(), entree_argent_poche.get(), entree_frequence.get(), fenetre_nouveau))
        bouton_valider.pack(pady=10)

    def valider_creation_nouveau_profil(self, prenom, solde, argent_poche, frequence, fenetre):
        """Valider la création du profil"""
        # Vérification que les champs sont remplis
        if not prenom or not solde or not argent_poche or not frequence:
            print("Tous les champs doivent être remplis.")
            return

        try:
            solde = float(solde)
            argent_poche = float(argent_poche)
        except ValueError:
            print("Les montants doivent être des nombres valides.")
            return

        # Si la validation est réussie, créer le profil
        nouvel_enfant = {
            "prenom": prenom,
            "solde": solde,
            "argent_poche": argent_poche,
            "frequence": frequence,
            "historique": []
        }
        self.profils.append(nouvel_enfant)

        # Mise à jour de l'affichage des profils
        self.afficher_profils()
        print(f"Profil de {prenom} créé avec un solde de {solde}€.")
        fenetre.destroy()

    def afficher_profil(self, i):
        """Afficher les détails d'un profil enfant"""
        enfant = self.profils[i]
        
        # Créer une nouvelle fenêtre pour afficher les détails
        profil_fenetre = tk.Toplevel()
        profil_fenetre.title(f"Profil de {enfant['prenom']}")
        
        # Affichage du solde
        tk.Label(profil_fenetre, text=f"Solde: {enfant['solde']}€").pack(pady=10)

        # Boutons d'actions
        bouton_ajout = tk.Button(profil_fenetre, text="AJOUT", command=lambda: self.ajouter_fonds(i))
        bouton_ajout.pack(pady=5)

        bouton_retrait = tk.Button(profil_fenetre, text="RETRAIT", command=lambda: self.retirer_fonds(i))
        bouton_retrait.pack(pady=5)

        bouton_historique = tk.Button(profil_fenetre, text="HISTORIQUE", command=lambda: self.afficher_historique(i))
        bouton_historique.pack(pady=5)

        bouton_editer = tk.Button(profil_fenetre, text="EDITER", command=lambda: self.editer_profil(i))
        bouton_editer.pack(pady=5)

    def ajouter_fonds(self, i):
        """Ajouter des fonds à un profil"""
        enfant = self.profils[i]
        montant_ajout = simpledialog.askfloat("Ajouter des fonds", "Montant à ajouter:")
        
        if montant_ajout is None:
            return  # L'utilisateur a annulé l'action
        
        enfant["solde"] += montant_ajout
        print(f"{montant_ajout}€ ajoutés au profil de {enfant['prenom']}.")

    def retirer_fonds(self, i):
        """Retirer des fonds du profil"""
        enfant = self.profils[i]
        montant_retrait = simpledialog.askfloat("Retirer des fonds", "Montant à retirer:")

        if montant_retrait is None:
            return  # L'utilisateur a annulé l'action

        if montant_retrait > enfant["solde"]:
            print("Solde insuffisant pour effectuer ce retrait.")
            return

        mode = self.demander_mode_paiement(enfant)

        # Effectuer le retrait en fonction du mode choisi
        if mode == "Cash":
            enfant["solde"] -= montant_retrait
        elif mode == "Paypal" and enfant.get("paypal"):
            enfant["solde"] -= montant_retrait
            print(f"Retrait effectué sur le compte PayPal de {enfant['prenom']}.")
        elif mode == "Banque" and enfant.get("iban"):
            enfant["solde"] -= montant_retrait
            print(f"Retrait effectué sur le compte bancaire de {enfant['prenom']}.")
        else:
            print("Mode de paiement invalide ou non renseigné.")

        # Mise à jour de l'affichage après retrait
        self.afficher_profil(i)

    def afficher_historique(self, i):
        """Afficher l'historique des transactions"""
        enfant = self.profils[i]
        
        # Créer une fenêtre pour afficher l'historique
        historique_fenetre = tk.Toplevel()
        historique_fenetre.title(f"Historique de {enfant['prenom']}")
        
        if enfant["historique"]:
            for transaction in enfant["historique"]:
                tk.Label(historique_fenetre, text=transaction).pack(pady=5)
        else:
            tk.Label(historique_fenetre, text="Aucune transaction effectuée.").pack(pady=10)

    def editer_profil(self, i):
        """Éditer un profil enfant"""
        enfant = self.profils[i]
        
        # Créer la fenêtre d'édition
        fenetre_editer = tk.Toplevel()
        fenetre_editer.title(f"Modifier le profil de {enfant['prenom']}")
        
        # Champs à éditer
        tk.Label(fenetre_editer, text="Prénom:").pack(pady=5)
        entree_prenom = tk.Entry(fenetre_editer)
        entree_prenom.insert(0, enfant["prenom"])
        entree_prenom.pack(pady=5)

        tk.Label(fenetre_editer, text="Solde:").pack(pady=5)
        entree_solde = tk.Entry(fenetre_editer)
        entree_solde.insert(0, str(enfant["solde"]))
        entree_solde.pack(pady=5)

        tk.Label(fenetre_editer, text="Argent de poche:").pack(pady=5)
        entree_argent_poche = tk.Entry(fenetre_editer)
        entree_argent_poche.insert(0, str(enfant["argent_poche"]))
        entree_argent_poche.pack(pady=5)

        tk.Label(fenetre_editer, text="Fréquence (hebdomadaire/mensuelle):").pack(pady=5)
        entree_frequence = tk.Entry(fenetre_editer)
        entree_frequence.insert(0, enfant["frequence"])
        entree_frequence.pack(pady=5)

        bouton_valider = tk.Button(fenetre_editer, text="Valider", command=lambda: self.valider_edition_profil(i, entree_prenom.get(), entree_solde.get(), entree_argent_poche.get(), entree_frequence.get(), fenetre_editer))
        bouton_valider.pack(pady=10)

    def valider_edition_profil(self, i, prenom, solde, argent_poche, frequence, fenetre):
        """Valider les modifications d'un profil"""
        if not prenom or not solde or not argent_poche or not frequence:
            print("Tous les champs doivent être remplis.")
            return

        try:
            solde = float(solde)
            argent_poche = float(argent_poche)
        except ValueError:
            print("Les montants doivent être des nombres valides.")
            return

        enfant = self.profils[i]
        enfant["prenom"] = prenom
        enfant["solde"] = solde
        enfant["argent_poche"] = argent_poche
        enfant["frequence"] = frequence

        self.afficher_profils()
        fenetre.destroy()
