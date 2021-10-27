import numpy as np
import random
import logging

from environnement import Environnement
from offre import Offre
from agent import Negociateur, Fournisseur, RED, RESET
from strategies import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NB_FOURNISSEURS = 50
NB_NEGOCIATEURS = 50


def main(NB_FOURNISSEURS, NB_NEGOCIATEURS):

    env = Environnement(NB_FOURNISSEURS, NB_NEGOCIATEURS)

    NB_ROUNDS = 25

    ########
    for round in range(NB_ROUNDS):
        print(f"---------- ROUND {round} ----------")
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
                        env.liste_fournisseurs[offre.fournisseur_id].deal = True
                        env.remove_negociateur(negociateur_id)
                        break
                    logger.debug(
                        f"N{negociateur.id} a proposé {prix_offre} pour F{offre.fournisseur_id}"
                    )
                    fournisseur = env.liste_fournisseurs[offre.fournisseur_id]
                    nouveau_prix = offre.liste_prix[negociateur_id]
                    prix_offre, deal = fournisseur.run(
                        round, negociateur_id, nouveau_prix
                    )
                    offre.update(negociateur_id, prix_offre, deal)
                    if deal:
                        env.liste_negociateurs[negociateur_id].deal = True
                        env.remove_negociateur(negociateur_id)
                        break
                    logger.debug(
                        f"F{fournisseur.id} a proposé {prix_offre} pour N{negociateur_id}"
                    )
                    logger.debug("\n")
    for negociateur in env.liste_negociateurs:
        if not negociateur.deal:
            print(f"{RED}No deal for N{negociateur.id}{RESET}")
    for fournisseur in env.liste_fournisseurs:
        if not fournisseur.deal:
            print(f"{RED}No deal for F{fournisseur.id}{RESET}")


if __name__ == "__main__":
    main(NB_FOURNISSEURS, NB_NEGOCIATEURS)
