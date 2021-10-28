import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


behaviors_dict = {
    "intransigeant": {
        "variation_rate_limit_price": 0.05,
        "new_offer_coefficient": 0.05,
    },
    "modere": {"variation_rate_limit_price": 0.15, "new_offer_coefficient": 0.15},
    "laxiste": {"variation_rate_limit_price": 0.30, "new_offer_coefficient": 0.30},
}

BLUE = "\033[94m"
WHITE = "\33[37m"
GREEN = "\33[32m"
RED = "\33[31m"
RESET = "\033[0m"


class Agent:
    def __init__(
        self, id, strategy, behavior, nb_opponents, limit_price, nb_max_offers=None
    ):
        self.id = id
        self.strategy = strategy  # function
        self.behavior_list = [
            behavior for i in range(nb_opponents)
        ]  # strings - key of the dictionnary
        # self.liste_offres = None  # list of offres objects
        self.offers_price_list = [None for i in range(nb_opponents)]
        if not nb_max_offers:
            self.nb_max_offers = random.randrange(10, 25)
        else:
            self.nb_max_offers = nb_max_offers
        self.deal = False
        self.limit_price_list = [limit_price for i in range(nb_opponents)]

    def _update_behavior(self, new_price, opponent_id, type):
        """The agent will be more inclined to make efforts if the opponent offers a price close to his limit price"""
        if type == "S":
            limit_price = self.limit_price_list[
                opponent_id
            ]  # limit price = minimum price
            delta_price = limit_price - new_price
        elif type == "B":
            limit_price = self.limit_price_list[
                opponent_id
            ]  # limit price = maximum price
            delta_price = new_price - limit_price
        behavior = self.behavior_list[opponent_id]
        if delta_price > 0:
            threshold_behavior = delta_price / limit_price
            if 0 < threshold_behavior <= 0.1:
                self.behavior_list[opponent_id] = "laxiste"
                logger.debug(f"{type}{self.id} passe de {behavior} à laxiste")
            elif 0.1 < threshold_behavior <= 0.2:
                self.behavior_list[opponent_id] = "modere"
                logger.debug(f"{type}{self.id} passe de {behavior} à modere")
            elif 0.2 < threshold_behavior:
                self.behavior_list[opponent_id] = "intransigeant"
                logger.debug(f"{type}{self.id} passe de {behavior} à intransigeant")


class Seller(Agent):
    """Le fournisseur souhaite vendre son service le plus cher possible et ne descendra pas sous un price minimal."""

    def __init__(
        self, id, strategy, behavior, nb_opponents, limit_price, nb_max_offers=None
    ):
        Agent.__init__(
            self, id, strategy, behavior, nb_opponents, limit_price, nb_max_offers
        )
        self.type = "S"

    def __str__(self):
        return f"""
        Fournisseur: {self.id}
        Strategie: {self.strategy.__name__}
        Comportements: {self.behavior_list}
        Prix max: {self.limit_price_list}
        Nb offres max: {self.nb_max_offers}"""

    def update_prix_min(self, current_round, opponent_id):
        behavior = self.behavior_list[opponent_id]
        variation_rate_limit_price = behaviors_dict[behavior][
            "variation_rate_limit_price"
        ]
        self.limit_price_list[opponent_id] *= (
            1
            - self.strategy(current_round / self.nb_max_offers)
            * variation_rate_limit_price
        )

    def make_new_offer(self, opponent_id):
        offer_price = self.offers_price_list[opponent_id]
        min_price = self.limit_price_list[opponent_id]
        if not offer_price:
            self.offers_price_list[opponent_id] = random.uniform(
                1.2 * min_price, 1.4 * min_price
            )
        else:
            behavior = self.behavior_list[opponent_id]
            new_offer_coefficient = behaviors_dict[behavior]["new_offer_coefficient"]
            self.offers_price_list[
                opponent_id
            ] = offer_price - new_offer_coefficient * (offer_price - min_price)
        logger.debug(f"Prix min F{self.id} : {min_price}")
        return self.offers_price_list[opponent_id]

    def is_satisfied(self, price, opponent_id):
        return self.limit_price_list[opponent_id] <= price

    def run(self, current_round, opponent_id, price):
        if not price:
            return self.make_new_offer(opponent_id), False
        elif self.is_satisfied(price, opponent_id):
            print(f"{BLUE}Deal entre F{self.id} et N{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            Agent._update_behavior(self, price, opponent_id, self.type)
            self.update_prix_min(current_round, opponent_id)
            return self.make_new_offer(opponent_id), False


class Buyer(Agent):
    """Le négociateur souhaite acheter le service le moins cher possible au fournisseur et s'est fixé un price maximal."""

    def __init__(
        self,
        id,
        strategy,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers=None,
    ):
        Agent.__init__(
            self, id, strategy, behavior, nb_opponents, limit_price, nb_max_offers
        )
        self.type = "B"

    def __str__(self):
        return f"""
        Negociateur: {self.id}
        Strategie: {self.strategy.__name__}
        Comportements: {self.behavior_list}
        Prix max: {self.limit_price_list}
        Nb offres max: {self.nb_max_offers}"""

    def update_prix_max(self, current_round, opponent_id):
        """L'agent sera plus enclin à faire des efforts si l'adversaire propose un price peu éloigné de son priux seuil"""
        behavior = self.behavior_list[opponent_id]
        variation_rate_limit_price = behaviors_dict[behavior][
            "variation_rate_limit_price"
        ]
        self.limit_price_list[opponent_id] *= (
            1
            + self.strategy(current_round / self.nb_max_offers)
            * variation_rate_limit_price
        )

    def make_new_offer(self, opponent_id):
        offer_price = self.offers_price_list[opponent_id]
        max_price = self.limit_price_list[opponent_id]
        if not offer_price:
            self.offers_price_list[opponent_id] = random.uniform(
                0.6 * max_price, 0.8 * max_price
            )
        else:
            behavior = self.behavior_list[opponent_id]
            new_offer_coefficient = behaviors_dict[behavior]["new_offer_coefficient"]
            self.offers_price_list[
                opponent_id
            ] = offer_price + new_offer_coefficient * (max_price - offer_price)
        logger.debug(f"Prix max N{self.id} : {max_price}")
        return self.offers_price_list[opponent_id]

    def is_satisfied(self, price, opponent_id):
        return price <= self.limit_price_list[opponent_id]

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return self.make_new_offer(opponent_id), False
        elif self.is_satisfied(price, opponent_id):
            print(f"{GREEN}Deal entre N{self.id} et F{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            Agent._update_behavior(self, price, opponent_id, self.type)
            self.update_prix_max(current_round, opponent_id)
            return self.make_new_offer(opponent_id), False
