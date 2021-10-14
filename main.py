import numpy as np
import random

random.seed(1)

comportements = {"intransigeant": 0.05, "modere": 0.15, "laxiste": 0.30}


class Environment:
    def __init__(self):
        self.fournisseurs = None  # dict
        self.negociateurs = None  # dict
        self.deals = None  # np.array


class Offres:
    def __init__(self, id, negociateur_id, fournisseur_id, prix):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.negociateur_id = negociateur_id
        self.prix = prix
        self.deal = False

    def update(self, nouveau_prix: float, deal: bool):
        self.prix = nouveau_prix
        self.deal = deal


class Fournisseur:
    def __init__(self, prix_min):
        self.prix_min = prix_min
        self.comportement = random.choice(list(comportements.keys()))
        self.nb_max_rounds = random.randrange(10, 20)
        self.critere_acceptation = 

    def is_satisfied(self, prix):
        return self.prix_min < prix

    def update_comportement(self, nouveau_prix):
        delta_prix =  nouveau_prix - self.prix_min
        if delta_prix > 0:
            threshold_comportement= delta_prix/self.prix_min
            if 0 < threshold_comportement < 5



    def baisse_exigence(self, prix):
        taux_decroissance = comportements[self.comportement]
        self.prix_min *= (1 - taux_decroissance) * (prix - self.prix_min)


class Negociateur:
    def __init__(self, prix, prix_max, nb_offres_max, taux_croissance):
        self.comportement = random.choice(list(comportements.keys()))
        self.nb_max_rounds = random.randrange(10, 20)
        self.prix = prix
        self.prix_max = prix_max
        self.nb_offres = 0

    def is_satisfied(self):
        return self.prix <= self.prix_max

    def new_offre(self):
        self.prix *= 1 + self.taux_croissance
        self.nb_offres += 1
        return self.prix

    def imbroglio(self):
        return self.nb_offres >= self.nb_offres_max


def main():

    env = Environment()
    env.fournisseurs = {}
    env.negociateurs = {}
    env.deals = np.zeros((len(env.fournisseurs), len(env.negociateurs)))

    nb_rounds = 10
    for round in nb_rounds:
        for fournisseur in env.fournisseurs:
            pass
        for negociateur in env.fournisseurs:
            pass

    negociateur = Negociateur(
        {
            "type": "avion",
            "prix": 630,
            "date_max_vente": "25/12",
            "date_depart": "01/01",
            "lieu_depart": "Limoges",
            "lieu_arrivee": "San Francisco",
        },
        prix_max=800,
        nb_offres_max=5,
        taux_croissance=0.1,
    )
    fournisseur = Fournisseur(
        {
            "type": "avion",
            "date_max_vente": "25/12",
            "date_depart": "01/01",
            "lieu_depart": "Limoges",
            "lieu_arrivee": "San Francisco",
        },
        prix_min=800,
        taux_decroissance=0.1,
    )

    for round in range(nb_rounds):
        if negociateur.imbroglio():
            return f"Echec de la négociation : {negociateur.nb_offres} offres effectuées, sans accord, nb_rounds =  {round}"

        if fournisseur.is_satisfied(negociateur.prix) and negociateur.is_satisfied():
            return f"Everyone is satisfied with price {negociateur.prix}, nb_rounds =  {round}"

        negociateur.new_offre()
        fournisseur.baisse_exigence()


if __name__ == "__main__":

    rv = main()
    print(rv)
