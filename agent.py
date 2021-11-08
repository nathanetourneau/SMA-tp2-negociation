import random
import logging
import scipy.stats as stats

logger = logging.getLogger(__name__)


behaviors_dict = {
    "intransigeant": {
        "variation_rate_limit_price": 0.01,
        "new_offer_coefficient": 0.05,
    },
    "modere": {"variation_rate_limit_price": 0.05, "new_offer_coefficient": 0.15},
    "laxiste": {"variation_rate_limit_price": 0.10, "new_offer_coefficient": 0.30},
}

BLUE = "\033[94m"
WHITE = "\33[37m"
GREEN = "\33[32m"
RED = "\33[31m"
RESET = "\033[0m"


def gaussian(x: float):
    return stats.norm.pdf(x, 0.5, 0.4)


class AgentRandom:
    def __init__(self, id, nb_opponents, limit_price, nb_max_offers):
        self.id = id
        self.nb_opponents = nb_opponents
        self.limit_price_list = [limit_price for i in range(nb_opponents)]
        self.nb_max_offers = nb_max_offers
        self.deal = False
        self.offers_price_list = [None for i in range(nb_opponents)]

    def _make_new_offer(self, opponent_id, agent_type):
        if agent_type == "B":
            self.offers_price_list[opponent_id] = random.uniform(
                0,
                self.limit_price_list[opponent_id],
            )
        elif agent_type == "S":
            self.offers_price_list[opponent_id] = random.uniform(
                self.limit_price_list[opponent_id],
                3 * self.limit_price_list[opponent_id],
            )
        return self.offers_price_list[opponent_id]

    def _is_satisfied(self, price, opponent_id, agent_type):
        if agent_type == "S":
            return self.limit_price_list[opponent_id] <= price
        elif agent_type == "B":
            return price <= self.limit_price_list[opponent_id]

    def _run(self, current_round, opponent_id, price, agent_type):
        if not price:
            return self._make_new_offer(opponent_id, agent_type), False
        elif self._is_satisfied(price, opponent_id, agent_type):
            if agent_type == "S":
                print(f"{BLUE}Deal between S{self.id} and B{opponent_id}!{RESET}")
            elif agent_type == "B":
                print(f"{GREEN}Deal between B{self.id} and S{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            return self._make_new_offer(opponent_id, agent_type), False


class SellerRandom(AgentRandom):
    def __init__(self, id, nb_opponents, limit_price, nb_max_offers):
        super().__init__(id, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "S"
        self.strategy = "random"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        return self._run(current_round, opponent_id, price, self.agent_type)


class BuyerRandom(AgentRandom):
    def __init__(self, id, nb_opponents, limit_price, nb_max_offers):
        super().__init__(id, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "B"
        self.strategy = "random"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        return self._run(current_round, opponent_id, price, self.agent_type)


class Agent:
    def __init__(self, id, behavior, nb_opponents, limit_price, nb_max_offers):
        self.id = id
        self.behavior_list = [behavior for i in range(nb_opponents)]
        self.offers_price_list = [None for i in range(nb_opponents)]
        self.nb_max_offers = nb_max_offers
        self.deal = False
        self.limit_price_list = [limit_price for i in range(nb_opponents)]

    def _update_behavior(self, new_price, opponent_id, agent_type):
        """The agent will be more inclined to make efforts if the opponent offers a price close to his limit price"""
        if agent_type == "S":
            limit_price = self.limit_price_list[
                opponent_id
            ]  # limit price = minimum price
            delta_price = limit_price - new_price
        elif agent_type == "B":
            limit_price = self.limit_price_list[
                opponent_id
            ]  # limit price = maximum price
            delta_price = new_price - limit_price
        behavior = self.behavior_list[opponent_id]
        if delta_price > 0:
            threshold_behavior = delta_price / limit_price
            if 0 < threshold_behavior <= 0.1:
                self.behavior_list[opponent_id] = "laxiste"
                print(f"{agent_type}{self.id} passe de {behavior} à laxiste")
            elif 0.1 < threshold_behavior <= 0.2:
                self.behavior_list[opponent_id] = "modere"
                print(f"{agent_type}{self.id} passe de {behavior} à modere")
            elif 0.2 < threshold_behavior:
                self.behavior_list[opponent_id] = "intransigeant"
                print(f"{agent_type}{self.id} passe de {behavior} à intransigeant")

    def _update_limit_price(self, opponent_id, current_round, agent_type):
        behavior = self.behavior_list[opponent_id]
        variation_rate_limit_price = behaviors_dict[behavior][
            "variation_rate_limit_price"
        ]
        if agent_type == "S":
            self.limit_price_list[opponent_id] *= (
                1
                - gaussian(current_round / self.nb_max_offers)
                * variation_rate_limit_price
            )
        elif agent_type == "B":
            self.limit_price_list[opponent_id] *= (
                1
                + gaussian(current_round / self.nb_max_offers)
                * variation_rate_limit_price
            )

    def _make_new_offer(self, opponent_id, agent_type):
        offer_price = self.offers_price_list[opponent_id]
        if agent_type == "S":
            min_price = self.limit_price_list[opponent_id]
            if not offer_price:
                self.offers_price_list[opponent_id] = random.uniform(
                    1.2 * min_price, 1.4 * min_price
                )
            else:
                behavior = self.behavior_list[opponent_id]
                new_offer_coefficient = behaviors_dict[behavior][
                    "new_offer_coefficient"
                ]
                self.offers_price_list[
                    opponent_id
                ] = offer_price - new_offer_coefficient * (offer_price - min_price)
            print(f"Min price S{self.id} : {min_price:.2f}")
        elif agent_type == "B":
            max_price = self.limit_price_list[opponent_id]
            if not offer_price:
                self.offers_price_list[opponent_id] = random.uniform(
                    0.6 * max_price, 0.8 * max_price
                )
            else:
                behavior = self.behavior_list[opponent_id]
                new_offer_coefficient = behaviors_dict[behavior][
                    "new_offer_coefficient"
                ]
                self.offers_price_list[
                    opponent_id
                ] = offer_price + new_offer_coefficient * (max_price - offer_price)
            print(f"Max price B{self.id} : {max_price:.2f}")
        return self.offers_price_list[opponent_id]

    def _is_satisfied(self, price, opponent_id, agent_type):
        if agent_type == "S":
            return self.limit_price_list[opponent_id] <= price
        elif agent_type == "B":
            return price <= self.limit_price_list[opponent_id]


class SellerLinear(Agent):
    def __init__(
        self,
        id,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers,
    ):
        super().__init__(id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "S"
        self.strategy = "linear"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return self._make_new_offer(opponent_id, self.agent_type), False
        elif self._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{BLUE}Deal between S{self.id} and B{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            return self._make_new_offer(opponent_id, self.agent_type), False


class BuyerLinear(Agent):
    def __init__(
        self,
        id,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers,
    ):
        super().__init__(id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "B"
        self.strategy = "linear"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return self._make_new_offer(opponent_id, self.agent_type), False
        elif self._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{GREEN}Deal between B{self.id} and S{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            return self._make_new_offer(opponent_id, self.agent_type), False


class SellerWithBehavior(Agent):
    def __init__(
        self,
        id,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers,
    ):
        super().__init__(id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "S"
        self.strategy = "behavior"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return self._make_new_offer(opponent_id, self.agent_type), False
        elif self._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{BLUE}Deal between S{self.id} and B{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            self._update_behavior(price, opponent_id, self.agent_type)
            return self._make_new_offer(opponent_id, self.agent_type), False


class BuyerWithBehavior(Agent):
    def __init__(
        self,
        id,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers,
    ):
        super().__init__(id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "B"
        self.strategy = "behavior"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return self._make_new_offer(opponent_id, self.agent_type), False
        elif self._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{GREEN}Deal between B{self.id} and S{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            self._update_behavior(price, opponent_id, self.agent_type)
            return self._make_new_offer(opponent_id, self.agent_type), False


class Seller(Agent):
    """Le fournisseur souhaite vendre son service le plus cher possible et ne descendra pas sous un prix minimal."""

    def __init__(self, id, behavior, nb_opponents, limit_price, nb_max_offers):
        Agent.__init__(self, id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "S"
        self.strategy = "gaussian"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return super()._make_new_offer(opponent_id, self.agent_type), False
        elif super()._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{BLUE}Deal between S{self.id} and B{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            super()._update_behavior(price, opponent_id, self.agent_type)
            super()._update_limit_price(opponent_id, current_round, self.agent_type)
            return self._make_new_offer(opponent_id, self.agent_type), False


class Buyer(Agent):
    """Le négociateur souhaite acheter le service le moins cher possible au fournisseur et s'est fixé un price maximal."""

    def __init__(
        self,
        id,
        behavior,
        nb_opponents,
        limit_price,
        nb_max_offers,
    ):
        Agent.__init__(self, id, behavior, nb_opponents, limit_price, nb_max_offers)
        self.agent_type = "B"
        self.strategy = "gaussian"
        print(f"Limit price {self.agent_type}{id} : {limit_price:.2f}")

    def run(self, current_round, opponent_id, price=None):
        if not price:
            return super()._make_new_offer(opponent_id, self.agent_type), False
        elif super()._is_satisfied(price, opponent_id, self.agent_type):
            print(f"{GREEN}Deal between B{self.id} and S{opponent_id}!{RESET}")
            self.deal = True
            return price, self.deal
        else:
            super()._update_behavior(price, opponent_id, self.agent_type)
            super()._update_limit_price(opponent_id, current_round, self.agent_type)
            return self._make_new_offer(opponent_id, self.agent_type), False
