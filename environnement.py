import random
from agent import Fournisseur, Negociateur
from offre import Offre
from strategies import *


class Environnement:
    def __init__(
        self,
        nb_fournisseurs,
        nb_negociateurs,
        liste_fournisseur_dict=None,
        liste_negociateur_dict=None,
    ):
        if liste_fournisseur_dict and liste_negociateur_dict:
            self.liste_fournisseurs = []
            self.liste_negociateurs = []
            for id, fdict in enumerate(liste_fournisseur_dict):
                strategie = fdict["strategie"]
                comportement = fdict["comportement"]
                prix_max = fdict["prix_seuil"]
                self.liste_fournisseurs.append(
                    Fournisseur(id, strategie, comportement, nb_negociateurs, prix_max)
                )
            for id, ndict in enumerate(liste_negociateur_dict):
                strategie = ndict["strategie"]
                comportement = ndict["comportement"]
                prix_min = ndict["prix_seuil"]
                self.liste_negociateurs.append(
                    Negociateur(id, strategie, comportement, nb_fournisseurs, prix_min)
                )
        else:
            self.liste_fournisseurs = [
                Fournisseur(
                    i, gaussienne, "modere", nb_negociateurs, random.randrange(100, 150)
                )
                for i in range(nb_fournisseurs)
            ]
            self.liste_negociateurs = [
                Negociateur(
                    i, gaussienne, "modere", nb_fournisseurs, random.randrange(50, 100)
                )
                for i in range(nb_negociateurs)
            ]
        self.liste_offres = []
        c = 0
        for i in range(nb_fournisseurs):
            self.liste_offres.append(Offre(c, i, [k for k in range(nb_negociateurs)]))
            c += 1

    def remove_negociateur(self, negociateur_id):
        for offre in self.liste_offres:
            offre.liste_negociateur_id.remove(negociateur_id)
