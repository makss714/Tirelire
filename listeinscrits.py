from tkinter import *

# Forme pour affichage de la liste des inscrits
def listeInscrit(fenetre, liste):
    newFen = Toplevel(fenetre)
    newFen.geometry("500x400+350+150")  # Taille ajustée pour plus d'espace
    newFen.title("Liste des inscrits")

    listeCan = Canvas(newFen, bg="#FF7800")
    fontLabel = 'arial 11 bold'

#Pour les entetes

    resultat = Label(listeCan, text="Liste des enfants inscrits :", font=fontLabel, fg="#FF7800", bg='white')
    header_prenom = Label(listeCan, text="Prénom", font=fontLabel, fg='white', bg="#FF7800")
    header_nom = Label(listeCan, text="Nom", font=fontLabel, fg='white', bg="#FF7800")
    header_montant = Label(listeCan, text="Montant de départ", font=fontLabel, fg='white', bg="#FF7800")
    header_hebdo = Label(listeCan, text="Argent hebdo", font=fontLabel, fg='white', bg="#FF7800")
    header_mens = Label(listeCan, text="Argent mensuel", font=fontLabel, fg='white', bg="#FF7800")
    header_paiement = Label(listeCan, text="Paiement", font=fontLabel, fg='white', bg="#FF7800")
    status = Label(listeCan, text="Aucun inscrit pour le moment", font='arial 9 bold', fg='white', bg="#FF7800")

#Placement des differentes entetes    
    
    listeCan.grid(row=0, column=0)
    resultat.grid(row=0, column=0, columnspan=6, pady=5)
    header_prenom.grid(row=1, column=0, padx=5, pady=5, sticky=W)
    header_nom.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    header_montant.grid(row=1, column=2, padx=5, pady=5, sticky=W)
    header_hebdo.grid(row=1, column=3, padx=5, pady=5, sticky=W)
    header_mens.grid(row=1, column=4, padx=5, pady=5, sticky=W)
    header_solde = Label(listeCan, text="Solde actuel", font=fontLabel, fg='white', bg="#FF7800")
    header_solde.grid(row=1, column=5, padx=5, pady=5, sticky=W)
    header_paiement.grid(row=1, column=5, padx=5, pady=5, sticky=W)
    status.grid(row=2, column=0, columnspan=6, pady=5)


    if liste:
        r = 3  # Ligne où commencer l'affichage des données
        for p in liste:
            solde_actuel = p.montant_depart #calcul pour implementer

            pre = Label(listeCan, text=p.prenom, font='arial 10', fg='white', bg="#FF7800")
            no = Label(listeCan, text=p.nom, font='arial 10', fg='white', bg="#FF7800")
            montant = Label(listeCan, text=p.montant_depart, font='arial 10', fg='white', bg="#FF7800")
            hebdo = Label(listeCan, text=p.argent_poche_hebdo, font='arial 10', fg='white', bg="#FF7800")
            mens = Label(listeCan, text=p.argent_poche_mens, font='arial 10', fg='white', bg="#FF7800")
            pai = Label(listeCan, text=p.paiement, font='arial 10', fg='white', bg="#FF7800")

#placement des donnees dans les colonnes correspondantes
            pre.grid(row=r, column=0, padx=5, pady=2, sticky=W)
            no.grid(row=r, column=1, padx=5, pady=2, sticky=W)
            montant.grid(row=r, column=2, padx=5, pady=2, sticky=W)
            hebdo.grid(row=r, column=3, padx=5, pady=2, sticky=W)
            mens.grid(row=r, column=4, padx=5, pady=2, sticky=W)
            solde = Label(listeCan, text=f"{solde_actuel:.2f} €", font='arial 10', fg='white', bg="#FF7800")
            solde.grid(row=r, column=5, padx=5, pady=2, sticky=W)
            pai.grid(row=r, column=5, padx=5, pady=2, sticky=W)

#on implemente le pour que les labels soient alignées au niveau de la fenetre et non supersposees
            r += 1 

#code pour mettre a jour le status            

        status.configure(text=f"{len(liste)} inscrit(s) pour le moment")
        status.grid(row=r, column=0, columnspan=6, pady=5)
    else:
        status.configure(text="Aucun inscrit pour le moment")

    newFen.mainloop()
