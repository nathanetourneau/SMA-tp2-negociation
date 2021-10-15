import numpy as np
import random

from environnement import Environnement
from offre import Offre
from agent import Negociateur, Fournisseur

random.seed(1)

comportements = {"intransigeant": 0.05, "modere": 0.15, "laxiste": 0.30}

# random.choice(list(comportements.keys()))


def main():

    env = Environnement()

    # TODO : instancier les agents/offres avec une boucle et un peu d'aléatoire

    env.liste_fournisseurs = []
    env.liste_negociateurs = []
    env.liste_offres = np.zeros((len(env.fournisseurs), len(env.negociateurs)))

    nb_rounds = 25

    # TODO: initialiser les offres, les négociateurs et les fournisseurs

########
    for round in range(nb_rounds):
        for negociateur in env.liste_negociateurs:
            for id_offre in negociateur.liste_offres:
                offre = env.offres[id_offre]
                if offre.deal:
                    continue
                prix = offre.prix

                if not negociateur.is_satisfied(id_offre, prix):
                    negociateur.faire_nouvelle_offre()

        for fournisseur in env.liste_fournisseurs:
            for id_offre in negociateur.offres:
                offre = env.offres[id_offre]
                if offre.deal:
                    continue
                prix = offre.prix

                if not fournisseur.is_satisfied(id_offre, prix):
                    fournisseur.faire_nouvelle_offre()

        for offre in env.offres:
            if negociateur.is_satisfied(offre.id_offre, offre.prix) and fournisseur.is_satisfied(id_offre, prix):
                offre.deal = True


if __name__ == "__main__":
    main()
