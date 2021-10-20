import numpy as np
import random

from environnement import Environnement
from offre import Offre
from agent import Negociateur, Fournisseur, NB_NEGOCIATEURS, NB_FOURNISSEURS
from strategies import *

# random.seed(1)

comportements = {"intransigeant": 0.05, "modere": 0.15, "laxiste": 0.30}

# random.choice(list(comportements.keys()))


def main(NB_FOURNISSEURS, NB_NEGOCIATEURS):

    env = Environnement()

    # TODO : instancier les agents/offres avec une boucle et un peu d'aléatoire

    NB_ROUNDS = 5

    # TODO: initialiser les offres, les négociateurs et les fournisseurs
    env.liste_fournisseurs = [
        Fournisseur(i, gaussienne, "modere", NB_NEGOCIATEURS, random.randrange(75, 125))
        for i in range(NB_FOURNISSEURS)
    ]
    env.liste_negociateurs = [
        Negociateur(i, gaussienne, "modere", NB_FOURNISSEURS, random.randrange(50, 100))
        for i in range(NB_FOURNISSEURS, NB_NEGOCIATEURS + NB_FOURNISSEURS)
    ]
    env.liste_offres = []
    c = 0
    for i in range(NB_FOURNISSEURS, NB_NEGOCIATEURS + NB_FOURNISSEURS):
        for j in range(NB_FOURNISSEURS):
            env.liste_offres.append(Offre(c, j, i))
            c += 1

    ########
    for round in range(NB_ROUNDS):
        print(f"----------------------- ROUND {round} -----------------------")
        for negociateur in env.liste_negociateurs:
            if not negociateur.deal:
                offres_negociateur = [
                    offre
                    for offre in env.liste_offres
                    if offre.negociateur_id == negociateur.id
                ]
                for offre in offres_negociateur:
                    nouveau_prix = offre.prix
                    prix_offre, deal = negociateur.run(
                        round, offre.fournisseur_id % NB_FOURNISSEURS, nouveau_prix
                    )
                    offre.update(prix_offre)
                    if deal:
                        break
                    print(
                        f"N{negociateur.id % NB_NEGOCIATEURS} a proposé {prix_offre} pour F{offre.fournisseur_id%NB_FOURNISSEURS}"
                    )
            print("\n")

        for fournisseur in env.liste_fournisseurs:
            if not fournisseur.deal:
                offres_fournisseur = [
                    offre
                    for offre in env.liste_offres
                    if offre.fournisseur_id == fournisseur.id
                ]
                for offre in offres_fournisseur:
                    nouveau_prix = offre.prix
                    prix_offre, deal = fournisseur.run(
                        round, offre.negociateur_id % NB_NEGOCIATEURS, nouveau_prix
                    )
                    offre.update(prix_offre)
                    if deal:
                        break
                    print(
                        f"F{fournisseur.id % NB_NEGOCIATEURS} a proposé {prix_offre} pour N{offre.negociateur_id%NB_NEGOCIATEURS}"
                    )
            print("\n")


if __name__ == "__main__":
    main(NB_FOURNISSEURS, NB_NEGOCIATEURS)
