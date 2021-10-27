import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


comportements_dict = {
    "intransigeant": {
        "taux_variation_prix_seuil": 0.05,
        "coefficient_nouvelle_offre": 0.05,
    },
    "modere": {"taux_variation_prix_seuil": 0.15, "coefficient_nouvelle_offre": 0.15},
    "laxiste": {"taux_variation_prix_seuil": 0.30, "coefficient_nouvelle_offre": 0.30},
}

BLUE = "\033[94m"
WHITE = "\33[37m"
GREEN = "\33[32m"
RED = "\33[31m"
RESET = "\033[0m"


class Agent:
    def __init__(self, id, strategie, comportement, nb_adversaires, nb_offres_max=None):
        self.id = id
        self.strategie = strategie  # function
        self.liste_comportements = [
            comportement for i in range(nb_adversaires)
        ]  # strings - key of the dictionnary
        # self.liste_offres = None  # list of offres objects
        self.liste_prix_offre = [None for i in range(nb_adversaires)]
        if not nb_offres_max:
            self.nb_offres_max = random.randrange(10, 25)
        else:
            self.nb_offres_max = nb_offres_max
        self.deal = False


class Fournisseur(Agent):
    """Le fournisseur souhaite vendre son service le plus cher possible et ne descendra pas sous un prix minimal."""

    def __init__(
        self, id, strategie, comportement, nb_adversaires, prix_min, nb_offres_max=None
    ):
        super().__init__(id, strategie, comportement, nb_adversaires, nb_offres_max)
        self.liste_prix_min = [prix_min for i in range(nb_adversaires)]

    def update_comportement(self, nouveau_prix, id_adversaire):
        """L'agent sera plus enclin à faire des efforts si l'adversaire propose un prix peu éloigné de son priux seuil"""
        prix_min = self.liste_prix_min[id_adversaire]
        delta_prix = prix_min - nouveau_prix
        comportement = self.liste_comportements[id_adversaire]
        if delta_prix > 0:
            threshold_comportement = delta_prix / prix_min
            if 0 < threshold_comportement <= 0.1:
                self.liste_comportements[id_adversaire] = "laxiste"
                logger.debug(f"F{self.id} passe de {comportement} à laxiste")
            elif 0.1 < threshold_comportement <= 0.2:
                self.liste_comportements[id_adversaire] = "modere"
                logger.debug(f"F{self.id} passe de {comportement} à modere")
            elif 0.2 < threshold_comportement:
                self.liste_comportements[id_adversaire] = "intransigeant"
                logger.debug(f"F{self.id} passe de {comportement} à intransigeant")

    def update_prix_min(self, current_round, id_adversaire):
        comportement = self.liste_comportements[id_adversaire]
        taux_variation_prix_seuil = comportements_dict[comportement][
            "taux_variation_prix_seuil"
        ]
        self.liste_prix_min[id_adversaire] *= (
            1
            - self.strategie(current_round / self.nb_offres_max)
            * taux_variation_prix_seuil
        )

    def faire_nouvelle_offre(self, id_adversaire):
        prix_offre = self.liste_prix_offre[id_adversaire]
        prix_min = self.liste_prix_min[id_adversaire]
        if not prix_offre:
            self.liste_prix_offre[id_adversaire] = random.uniform(
                1.2 * prix_min, 1.4 * prix_min
            )
        else:
            comportement = self.liste_comportements[id_adversaire]
            coefficient_nouvelle_offre = comportements_dict[comportement][
                "coefficient_nouvelle_offre"
            ]
            self.liste_prix_offre[
                id_adversaire
            ] = prix_offre - coefficient_nouvelle_offre * (prix_offre - prix_min)
        logger.debug(f"Prix min F{self.id} : {prix_min}")
        return self.liste_prix_offre[id_adversaire]

    def is_satisfied(self, prix, id_adversaire):
        return self.liste_prix_min[id_adversaire] <= prix

    def run(self, current_round, id_adversaire, prix):
        if not prix:
            return self.faire_nouvelle_offre(id_adversaire), False
        elif self.is_satisfied(prix, id_adversaire):
            print(f"{BLUE}Deal entre F{self.id} et N{id_adversaire}!{RESET}")
            self.deal = True
            return prix, self.deal
        else:
            self.update_comportement(prix, id_adversaire)
            self.update_prix_min(current_round, id_adversaire)
            return self.faire_nouvelle_offre(id_adversaire), False


class Negociateur(Agent):
    """Le négociateur souhaite acheter le service le moins cher possible au fournisseur et s'est fixé un prix maximal."""

    def __init__(
        self, id, strategie, comportement, nb_adversaires, prix_max, nb_offres_max=None
    ):
        super().__init__(id, strategie, comportement, nb_adversaires, nb_offres_max)
        self.liste_prix_max = [prix_max for i in range(nb_adversaires)]

    def update_comportement(self, nouveau_prix, id_adversaire):
        """L'agent sera plus enclin à faire des efforts si l'adversaire propose un prix peu éloigné de son priux seuil"""
        prix_max = self.liste_prix_max[id_adversaire]
        delta_prix = nouveau_prix - prix_max
        comportement = self.liste_comportements[id_adversaire]
        if delta_prix > 0:
            threshold_comportement = delta_prix / prix_max
            if 0 < threshold_comportement <= 0.1:
                self.liste_comportements[id_adversaire] = "laxiste"
                logger.debug(f"N{self.id} passe de {comportement} à laxiste")
            elif 0.1 < threshold_comportement <= 0.2:
                self.liste_comportements[id_adversaire] = "modere"
                logger.debug(f"N{self.id} passe de {comportement} à modere")
            elif 0.2 < threshold_comportement:
                self.liste_comportements[id_adversaire] = "intransigeant"
                logger.debug(f"N{self.id} passe de {comportement} à intransigeant")

    def update_prix_max(self, current_round, id_adversaire):
        """L'agent sera plus enclin à faire des efforts si l'adversaire propose un prix peu éloigné de son priux seuil"""
        comportement = self.liste_comportements[id_adversaire]
        taux_variation_prix_seuil = comportements_dict[comportement][
            "taux_variation_prix_seuil"
        ]
        self.liste_prix_max[id_adversaire] *= (
            1
            + self.strategie(current_round / self.nb_offres_max)
            * taux_variation_prix_seuil
        )

    def faire_nouvelle_offre(self, id_adversaire):
        prix_offre = self.liste_prix_offre[id_adversaire]
        prix_max = self.liste_prix_max[id_adversaire]
        if not prix_offre:
            self.liste_prix_offre[id_adversaire] = random.uniform(
                0.6 * prix_max, 0.8 * prix_max
            )
        else:
            comportement = self.liste_comportements[id_adversaire]
            coefficient_nouvelle_offre = comportements_dict[comportement][
                "coefficient_nouvelle_offre"
            ]
            self.liste_prix_offre[
                id_adversaire
            ] = prix_offre + coefficient_nouvelle_offre * (prix_max - prix_offre)
        logger.debug(f"Prix max N{self.id} : {prix_max}")
        return self.liste_prix_offre[id_adversaire]

    def is_satisfied(self, prix, id_adversaire):
        return prix <= self.liste_prix_max[id_adversaire]

    def run(self, current_round, id_adversaire, prix=None):
        if not prix:
            return self.faire_nouvelle_offre(id_adversaire), False
        elif self.is_satisfied(prix, id_adversaire):
            print(f"{GREEN}Deal entre N{self.id} et F{id_adversaire}!{RESET}")
            self.deal = True
            return prix, self.deal
        else:
            self.update_comportement(prix, id_adversaire)
            self.update_prix_max(current_round, id_adversaire)
            return self.faire_nouvelle_offre(id_adversaire), False
