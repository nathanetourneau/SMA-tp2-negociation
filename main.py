import numpy as np
import random

from environnement import Environnement
from offre import Offre
from agent import Negociateur, Fournisseur
from strategies import *

random.seed(1)

comportements = {"intransigeant": 0.05, "modere": 0.15, "laxiste": 0.30}

# random.choice(list(comportements.keys()))


def main():

    env = Environnement()

    # TODO : instancier les agents/offres avec une boucle et un peu d'aléatoire

    NB_ROUNDS = 25
    NB_FOURNISSEURS = 5
    NB_NEGOCIATEURS = 5

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
    for round in range(1):
        for negociateur in env.liste_negociateurs:
            if not negociateur.deal:
                offres_negociateur = [
                    offre
                    for offre in env.liste_offres
                    if offre.negociateur_id == negociateur.id
                ]
                for offre in offres_negociateur:
                    nouveau_prix = offre.prix
                    prix_offre = negociateur.run(
                        round, offre.fournisseur_id, nouveau_prix
                    )
                    print(
                        f"Negociateur {negociateur.id} a proposé {prix_offre:0.1f} pour offre {offre.fournisseur_id}"
                    )
                    offre.update(prix_offre)
            print("\n")

            # if offre.deal:
            #     continue
            # prix = offre.prix

        #         if not negociateur.is_satisfied(id_offre, prix):
        #             negociateur.faire_nouvelle_offre()

        # for fournisseur in env.liste_fournisseurs:
        #     for id_offre in negociateur.offres:
        #         offre = env.offres[id_offre]
        #         if offre.deal:
        #             continue
        #         prix = offre.prix

        #         if not fournisseur.is_satisfied(id_offre, prix):
        #             fournisseur.faire_nouvelle_offre()

        # for offre in env.offres:
        #     if negociateur.is_satisfied(
        #         offre.id_offre, offre.prix
        #     ) and fournisseur.is_satisfied(id_offre, prix):
        #         offre.deal = True


if __name__ == "__main__":
    main()
