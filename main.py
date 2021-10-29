import numpy as np
import random
import logging

from environnement import Environment
from offre import Offre
from agent import Buyer, Seller, RED, RESET
from strategies import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NB_SELLERS = 2
NB_BUYERS = 2
NB_ROUNDS = 25

if __name__ == "__main__":

    # sellers_dict_list = [{"strategy": gaussian, "behavior": "modere", "limit_price": 100}]

    env = Environment(NB_SELLERS, NB_BUYERS, NB_ROUNDS, "complex")
    env.run()
    for buyer in env.buyers_list:
        if not buyer.deal:
            print(f"{RED}No deal for N{buyer.id}{RESET}")
    for seller in env.sellers_list:
        if not seller.deal:
            print(f"{RED}No deal for F{seller.id}{RESET}")
