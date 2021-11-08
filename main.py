import numpy as np
import matplotlib.pyplot as plt
import logging
from collections import Counter


from environnement import Environment


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


"""
STRATEGY can be :
- random for random agents only
- linear for linear agents only
- behavior for agents with behavior variation
- gaussian for limit price variation based on the timeline of the negotiation
- mixed for 4*N sellers and 4*M buyers (N & M of each strategy) PLESE SPECIFY A MULTIPLE OF 4 FOR NB_BUYERS AND NB_SELLERS
"""
##### PARAMETERS #####
STRATEGY = "random"
NB_SELLERS = 5
NB_BUYERS = 5
NB_ROUNDS = 10
######################


def run_negotiations(strategy, nb_sellers, nb_buyers, nb_rounds):
    # deal_rate_list = []
    # average_rounds_before_deal = []
    nb_deals = 0
    env = Environment(nb_sellers, nb_buyers, nb_rounds, strategy)
    env.run()
    for seller in env.sellers_list:
        if seller.deal:
            nb_deals += 1
    metrics = env.env_metrics()

    print(
        f"\33[31m{2*len(metrics.deals['couples'])} DEALS OUT OF {NB_BUYERS+NB_SELLERS} AGENTS\033[0m"
    )

    return metrics.deals["strategies"]


def run_multiple_negotiations(strategy, nb_sellers, nb_buyers, nb_rounds, plot=True):
    """Performs multiple negotiations between a given number of agents and a given strategy. Returns the metrics counting the deals for each agent."""
    strategies_with_deal = []
    for k in range(1000):
        strategies_with_deal += run_negotiations(
            strategy, nb_sellers, nb_buyers, nb_rounds
        )
    if plot:
        plot_histogram_from_string_list(strategies_with_deal)


def plot_histogram_from_string_list(liste):
    """Allow to plot the histogram representing the number of deals as a function of the strategy adopted"""
    counts = Counter(liste)
    common = counts.most_common()
    labels = [item[0] for item in common]
    number = [item[1] for item in common]
    nbars = len(common)

    plt.bar(np.arange(nbars), number, tick_label=labels)
    plt.show()


def plot_negotiation(metrics, deal: bool):
    """PLots the eviolution of price limit and price offers between two agents across the negotiation rounds"""
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
        if deal:
            plt.axvline(x=x - 1, color="r")
    plt.show()


def run_negotiation_between_two_agents(strategy, nb_rounds, plot=True):
    """
    Performs a negotiation between two agents for a given strategy to simply visualize how it works
    """
    if strategy == "mixed":
        raise Exception("Cannot use this function with 'mixed' strategy")

    env = Environment(1, 1, nb_rounds, strategy)
    env.run()
    metrics = env.env_metrics()
    if metrics.deals["strategies"]:
        deal = True
    else:
        deal = False
    if plot:
        plot_negotiation(metrics, deal)

    return deal


def deal_rate_between_two_agents(strategy):
    """Performs 10 000 negotiations between two agents to measure the deal rate of a given strategy"""
    deal_list = []
    for k in range(10000):
        deal_list.append(run_negotiation_between_two_agents(strategy, 10, plot=False))
    return sum(deal_list) * 100 / 10000


if __name__ == "__main__":
    run_negotiations(STRATEGY, NB_SELLERS, NB_BUYERS, NB_ROUNDS)

    # run_multiple_negotiations(STRATEGY, NB_SELLERS, NB_BUYERS, NB_ROUNDS)

    # run_negotiation_between_two_agents(STRATEGY, NB_ROUNDS, plot=False)

    # print(
    #     f"\n\nDeal rate for strategy '{STRATEGY}' : {deal_rate_between_two_agents(STRATEGY)}%"
    # )
