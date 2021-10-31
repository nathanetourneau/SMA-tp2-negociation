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

# NB_SELLERS = random.randint(5, 15)
# NB_BUYERS = random.randint(5, 15)
# NB_ROUNDS = 1
STRATEGY = "linear"
NB_TRY = 50
# Strategy can be :  'random', 'linear', 'complex','complex+'
strategies_list = ["random", "linear", "complex", "complex+"]


def eval(strategy):
    NB_SELLERS = 10
    NB_BUYERS = 10
    NB_ROUNDS = 5
    deal_rate_list = {}
    average_rounds_before_deal = {}
    for strategy in strategies_list:
        deal_rate_list[strategy] = []
        average_rounds_before_deal[strategy] = []
    for i in range(NB_TRY):
        for strategy in strategies_list:
            nb_deals = 0
            env = Environment(NB_SELLERS, NB_BUYERS, NB_ROUNDS, strategy)
            env.run()
            average_rounds_before_deal[strategy].append(
                env.average_nb_rounds_before_deal()
            )
            for seller in env.sellers_list:
                if seller.deal:
                    nb_deals += 1
            deal_rate_list[strategy].append(nb_deals / NB_SELLERS)
    return deal_rate_list, average_rounds_before_deal


if __name__ == "__main__":
    # env = Environment(NB_SELLERS, NB_BUYERS, NB_ROUNDS, STRATEGY)
    # env.run()
    # for buyer in env.buyers_list:
    #     if not buyer.deal:
    #         print(f"{RED}No deal for N{buyer.id}{RESET}")
    # for seller in env.sellers_list:
    #     if not seller.deal:
    #         print(f"{RED}No deal for F{seller.id}{RESET}")

    deal_rate_list, average_rounds_before_deal = eval(STRATEGY)
    # print(np.average(deal_rate_list))
    s = 10
    # plt.plot(range(100), deal_rate_list["random"],s=s color="k")
    # plt.plot(range(100), deal_rate_list["linear"], s=s,color="r")
    # plt.scatter(
    #     range(NB_TRY), deal_rate_list["complex"], s=s, color="orange", label="complex"
    # )
    # plt.scatter(
    #     range(NB_TRY), deal_rate_list["complex+"], s=s, color="b", label="complex+"
    # )
    plt.plot(
        range(NB_TRY),
        average_rounds_before_deal["complex"],
        color="r",
        label="complex",
    )
    plt.plot(
        range(NB_TRY),
        average_rounds_before_deal["complex+"],
        color="b",
        label="complex+",
    )
    plt.legend()
    plt.show()
