import numpy as np
import matplotlib.pyplot as plt
import random
import logging

from environnement import Environment
from offre import Offre
from agent import Buyer, Seller, RED, RESET


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NB_SELLERS = random.randint(5, 15)
# NB_BUYERS = random.randint(5, 15)
# NB_ROUNDS = 1
STRATEGY = "linear"
# Strategy can be :  'random', 'linear', 'complex'


def eval(strategy):
    NB_SELLERS = 10
    NB_BUYERS = 10
    NB_ROUNDS = 5
    deal_rate_list = []
    for i in range(100):
        nb_deals = 0
        env = Environment(NB_SELLERS, NB_BUYERS, NB_ROUNDS, strategy)
        env.run()
        for seller in env.sellers_list:
            if seller.deal:
                nb_deals += 1
        # print(nb_deals, NB_SELLERS, nb_deals / NB_SELLERS)
        deal_rate_list.append(nb_deals / NB_SELLERS)
    return deal_rate_list


if __name__ == "__main__":
    # env = Environment(NB_SELLERS, NB_BUYERS, NB_ROUNDS, STRATEGY)
    # env.run()
    # for buyer in env.buyers_list:
    #     if not buyer.deal:
    #         print(f"{RED}No deal for N{buyer.id}{RESET}")
    # for seller in env.sellers_list:
    #     if not seller.deal:
    #         print(f"{RED}No deal for F{seller.id}{RESET}")

    deal_rate_list = eval(STRATEGY)
    print(np.average(deal_rate_list))
    # plt.plot(range(100), deal_rate_list, color="k")
    plt.scatter(range(100), deal_rate_list, color="b")
    plt.show()
