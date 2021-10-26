import numpy as np
import random
import logging

from environnement import Environnement
from offre import Offre
from agent import Negociateur, Fournisseur, NB_NEGOCIATEURS, NB_FOURNISSEURS
from strategies import *

random.seed(1)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# random.choice(list(comportements.keys()))


def main(NB_FOURNISSEURS, NB_NEGOCIATEURS):

    env = Environnement()

    NB_ROUNDS = 15

    env.liste_fournisseurs = [
        Fournisseur(i, gaussienne, "modere", NB_NEGOCIATEURS, random.randrange(75, 125))
        for i in range(NB_FOURNISSEURS)
    ]
    env.liste_negociateurs = [
        Negociateur(i, gaussienne, "modere", NB_FOURNISSEURS, random.randrange(50, 100))
        for i in range(NB_NEGOCIATEURS)
    ]
    env.liste_offres = []
    c = 0
    for i in range(NB_FOURNISSEURS):
        env.liste_offres.append(Offre(c, i, [k for k in range(NB_NEGOCIATEURS)]))
        c += 1

    ########
    for round in range(NB_ROUNDS):
        print(f"----------------------- ROUND {round} -----------------------")
        for offre in env.liste_offres:
            if not offre.deal:
                for negociateur_id in offre.liste_negociateur_id:
                    negociateur = env.liste_negociateurs[negociateur_id]
                    nouveau_prix = offre.liste_prix[negociateur_id]
                    prix_offre, deal = negociateur.run(
                        round, offre.fournisseur_id, nouveau_prix
                    )
                    offre.update(negociateur_id, prix_offre, deal)
                    if deal:
                        env.remove_negociateur(negociateur_id)
                        break
                    print(
                        f"N{negociateur.id} a proposé {prix_offre} pour F{offre.fournisseur_id}"
                    )
                    fournisseur = env.liste_fournisseurs[offre.fournisseur_id]
                    nouveau_prix = offre.liste_prix[negociateur_id]
                    prix_offre, deal = fournisseur.run(
                        round, negociateur_id, nouveau_prix
                    )
                    offre.update(negociateur_id, prix_offre, deal)
                    if deal:
                        env.remove_negociateur(negociateur_id)
                        break
                    print(
                        f"F{fournisseur.id} a proposé {prix_offre} pour N{negociateur_id}"
                    )
                    print("\n")

        # for negociateur in env.liste_negociateurs:
        #     if not negociateur.deal:
        #         offres_negociateur = [
        #             offre
        #             for offre in env.liste_offres
        #             if (offre.negociateur_id == negociateur.id) and (not offre.deal)
        #         ]
        #         for offre in offres_negociateur:
        #             nouveau_prix = offre.prix
        #             prix_offre, deal = negociateur.run(
        #                 round, offre.fournisseur_id % NB_FOURNISSEURS, nouveau_prix
        #             )
        #             offre.update(negociateur.id, prix_offre)
        #             if deal:
        #                 offre.deal = True
        #                 break
        #             print(
        #                 f"N{negociateur.id % NB_NEGOCIATEURS} a proposé {prix_offre} pour F{offre.fournisseur_id%NB_FOURNISSEURS}"
        #             )
        #     print("\n")

        # for fournisseur in env.liste_fournisseurs:
        #     if not fournisseur.deal:
        #         offres_fournisseur = [
        #             offre
        #             for offre in env.liste_offres
        #             if offre.fournisseur_id == fournisseur.id
        #         ]
        #         for offre in offres_fournisseur:
        #             nouveau_prix = offre.prix
        #             prix_offre, deal = fournisseur.run(
        #                 round, offre.negociateur_id % NB_NEGOCIATEURS, nouveau_prix
        #             )
        #             offre.update(prix_offre)
        #             if deal:
        #                 break
        #             print(
        #                 f"F{fournisseur.id % NB_NEGOCIATEURS} a proposé {prix_offre} pour N{offre.negociateur_id%NB_NEGOCIATEURS}"
        #             )
        #     print("\n")


if __name__ == "__main__":
    main(NB_FOURNISSEURS, NB_NEGOCIATEURS)
