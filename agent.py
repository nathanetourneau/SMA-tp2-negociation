import random

comportements_dict = {"intransigeant": {"taux_variation_prix_seuil": 0.05, "coefficient_nouvelle_offre": 0.05},
                      "modere": {"taux_variation_prix_seuil": 0.15, "coefficient_nouvelle_offre": 0.15},
                      "laxiste": {"taux_variation_prix_seuil": 0.30, "coefficient_nouvelle_offre": 0.30}}

# random.choice(list(comportements.keys()))


class Agent:
    def __init__(self, id, strategie, comportement, nb_offres_max=None):
        self.id = id
        self.strategie = strategie
        self.comportement = comportement
        self.liste_offres = None
        self.dernier_prix_propose = None
        if not nb_offres_max:
            self.nb_offres_max = random.randrange(10, 25)
        else:
            self.nb_offres_max = nb_offres_max

    def strategie_gaussienne(self):
        """On va définir la st"""
        if self.strategie == "gaussienne":
            pass


class Fournisseur(Agent):
    """Le fournisseur souhaite vendre son service le plus cher possible et ne descendra pas sous un prix minimal."""

    def __init__(self, id, comportement, prix_min, nb_offres_max=None):
        super(Fournisseur, self).__init__(id, comportement, nb_offres_max)
        self.prix_min = prix_min
        self.taux_croissance_offre = comportements_dict[self.comportement]

    def update_comportement(self, nouveau_prix):
        delta_prix = nouveau_prix - self.prix_min
        if delta_prix > 0:
            threshold_comportement = delta_prix/self.prix_min
            if 0 < threshold_comportement < 5:
                pass

    def update_prix_min(self, round_actuel):
        taux_variation_prix_seuil = comportements_dict[self.comportement]["taux_variation_prix_seuil"]
        self.prix_min *= 1 + \
            self.strategie(round_actuel/self.nb_offres_max) * \
            taux_variation_prix_seuil

    def faire_nouvelle_offre(self):
        coefficient_nouvelle_offre = comportements_dict[self.comportement]["coefficient_nouvelle_offre"]
        self.prix *= 1 - coefficient_nouvelle_offre
        return self.prix

    def is_satisfied(self):
        return self.prix_min <= self.prix


class Negociateur(Agent):
    """Le négociateur souhaite acheter le service le moins cher possible au fournisseur et s'est fixé un prix maximal."""

    def __init__(self, id, comportement, prix_max, nb_offres_max=None):
        super(Negociateur, self).__init__(id, comportement, nb_offres_max)
        self.prix_max = prix_max

    def is_satisfied(self):
        return self.prix <= self.prix_max

    def update_prix_max(self, round_actuel):
        taux_variation_prix_seuil = comportements_dict[self.comportement]["taux_variation_prix_seuil"]
        self.prix_max *= 1 - \
            self.strategie(round_actuel/self.nb_offres_max) * \
            taux_variation_prix_seuil

    def faire_nouvelle_offre(self):
        coefficient_nouvelle_offre = comportements_dict[self.comportement]["coefficient_nouvelle_offre"]
        self.prix *= 1 + coefficient_nouvelle_offre
        return self.prix
