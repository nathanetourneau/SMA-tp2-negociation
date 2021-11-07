import numpy as np
import matplotlib.pyplot as plt
import random
import logging

from numpy.lib.function_base import average

from environnement import Environment
from offre import Offre
from agent import Buyer, Seller, RED, RESET


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STRATEGY = "gaussian"
NB_TESTS = 1
NB_SELLERS = 1
NB_BUYERS = 1
NB_ROUNDS = 10
"""
STRATEGY can be :
- random for random agents only
- linear for linear agents only
- behavior for agents with behavior variation
- gaussian for limit price variation based on the timeline of the negotiation
- mixed for 8 sellers and 8 buyers (2 of each strategy)
"""


def eval(strategy, nb_sellers, nb_buyers, nb_rounds, nb_tests):
    strategies_list = ["random", "linear", "behavior", "gaussian"]
    deal_rate_list = []
    average_rounds_before_deal = []
    for i in range(nb_tests):
        nb_deals = 0
        env = Environment(nb_sellers, nb_buyers, nb_rounds, strategy)
        env.run()
        for seller in env.sellers_list:
            if seller.deal:
                nb_deals += 1
        deal_rate_list.append(nb_deals / NB_SELLERS)
    return deal_rate_list, average_rounds_before_deal


def plot_negotiation_between_two_agents(strategy, nb_rounds):
    env = Environment(1, 1, nb_rounds, strategy)
    env.run()
    metrics = env.env_metrics()
    seller_limit_prices = metrics.sellers_limit_prices["0"]
    seller_offers = metrics.sellers_offers["0"]
    buyer_limit_prices = metrics.buyers_limit_prices["0"]
    buyer_offers = metrics.buyers_offers["0"]
    x = len(seller_offers)

    if len(seller_offers):
        plt.plot(
            range(len(seller_offers)),
            seller_offers,
            "o-",
            label="Seller offers",
            color="b",
        )
        plt.plot(
            range(len(seller_limit_prices)),
            seller_limit_prices,
            "o--",
            label="Seller min prices",
            color="b",
        )
        plt.plot(
            range(len(buyer_offers)),
            buyer_offers,
            "o-",
            label="Buyer offers",
            color="k",
        )
        plt.plot(
            range(len(buyer_limit_prices)),
            buyer_limit_prices,
            "o--",
            label="Buyer max prices",
            color="k",
        )
        plt.legend()
        plt.xlabel("Round")
        plt.xlim([0, 10])
        if x < nb_rounds:
            plt.axvline(x=x - 1, color="r")
        plt.show()


if __name__ == "__main__":
    plot_negotiation_between_two_agents(STRATEGY, NB_ROUNDS)
    # deal_rate_list, average_rounds_before_deal = eval(
    #     STRATEGY, NB_SELLERS, NB_BUYERS, NB_ROUNDS, NB_TESTS
    # )

    # s = 10
    # plt.plot(
    #     range(NB_TESTS),
    #     average_rounds_before_deal["complex"],
    #     color="r",
    #     label="complex",
    # )
    # plt.plot(
    #     range(NB_TESTS),
    #     average_rounds_before_deal["complex+"],
    #     color="b",
    #     label="complex+",
    # )
    # plt.legend()
    # plt.show()
