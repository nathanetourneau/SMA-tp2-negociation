import random
import time
from agent import *
from offre import Offre
import logging
import numpy as np
from metrics import Metrics

logger = logging.getLogger()


class Environment:
    def __init__(self, nb_sellers, nb_buyers, nb_rounds, strategy):
        self.metrics = Metrics(nb_sellers, nb_buyers)

        self.nb_rounds = nb_rounds
        # nb_max_offers = random.randint(nb_rounds // 2, nb_rounds)
        nb_max_offers = nb_rounds
        behavior = "modere"
        if strategy == "gaussian":
            self.sellers_list = [
                Seller(
                    i,
                    behavior,
                    nb_buyers,
                    random.randrange(80, 120),
                    nb_max_offers,
                )
                for i in range(nb_sellers)
            ]
            self.buyers_list = [
                Buyer(i, behavior, nb_sellers, random.randrange(80, 120), nb_max_offers)
                for i in range(nb_buyers)
            ]

        elif strategy == "behavior":
            self.sellers_list = [
                SellerWithBehavior(
                    i,
                    behavior,
                    nb_buyers,
                    random.randrange(80, 120),
                    nb_max_offers,
                )
                for i in range(nb_sellers)
            ]
            self.buyers_list = [
                BuyerWithBehavior(
                    i, behavior, nb_sellers, random.randrange(80, 120), nb_max_offers
                )
                for i in range(nb_buyers)
            ]

        elif strategy == "linear":
            self.sellers_list = [
                SellerLinear(
                    i,
                    behavior,
                    nb_buyers,
                    random.randrange(80, 120),
                    nb_max_offers,
                )
                for i in range(nb_sellers)
            ]
            self.buyers_list = [
                BuyerLinear(
                    i, behavior, nb_sellers, random.randrange(80, 120), nb_max_offers
                )
                for i in range(nb_buyers)
            ]

        elif strategy == "random":
            self.sellers_list = [
                SellerRandom(i, nb_buyers, random.randrange(80, 120), nb_max_offers)
                for i in range(nb_sellers)
            ]
            self.buyers_list = [
                BuyerRandom(i, nb_sellers, random.randrange(80, 120), nb_max_offers)
                for i in range(nb_buyers)
            ]

        elif strategy == "mixed":
            if (nb_sellers % 4 == 0) and (nb_buyers % 4 == 0):
                self.sellers_list = []
                self.buyers_list = []
                for i in range(nb_sellers):
                    if 0 <= i < nb_sellers // 4:
                        self.sellers_list.append(
                            SellerRandom(
                                i,
                                nb_buyers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    elif nb_sellers // 4 <= i < nb_sellers // 2:
                        self.sellers_list.append(
                            SellerLinear(
                                i,
                                behavior,
                                nb_buyers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    elif nb_sellers // 2 <= i < nb_sellers // 4 * 3:
                        self.sellers_list.append(
                            SellerWithBehavior(
                                i,
                                behavior,
                                nb_buyers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    elif nb_sellers // 4 * 3 <= i < nb_sellers:
                        self.sellers_list.append(
                            Seller(
                                i,
                                behavior,
                                nb_buyers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    else:
                        raise Exception("bug seller")

                for i in range(nb_buyers):
                    if 0 <= i < nb_buyers // 4:
                        self.buyers_list.append(
                            BuyerRandom(
                                i, nb_sellers, random.randrange(80, 120), nb_max_offers
                            )
                        )
                    elif nb_buyers // 4 <= i < nb_buyers // 2:
                        self.buyers_list.append(
                            BuyerLinear(
                                i,
                                behavior,
                                nb_sellers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    elif nb_buyers // 2 <= i < nb_buyers // 4 * 3:
                        self.buyers_list.append(
                            BuyerWithBehavior(
                                i,
                                behavior,
                                nb_sellers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    elif nb_buyers // 4 * 3 <= i < nb_buyers:
                        self.buyers_list.append(
                            Buyer(
                                i,
                                behavior,
                                nb_sellers,
                                random.randrange(80, 120),
                                nb_max_offers,
                            )
                        )
                    else:
                        raise Exception("bug buyer")

            else:
                raise Exception(
                    "Please specify a multiple of 4 for nb_buyers and nb_sellers, so that there's the same number of agents for each strategy."
                )

        else:
            raise Exception("Please specify a strategy")

        self.liste_offres = []
        c = 0
        for i in range(nb_sellers):
            self.liste_offres.append(Offre(c, i, [k for k in range(nb_buyers)]))
            c += 1

    def remove_buyer_from_offer(self, negociateur_id):
        for offre in self.liste_offres:
            offre.buyers_id_list.remove(negociateur_id)

    def run(self):
        """
        Iterates over the number of rounds defined in the main file.
        For each round, it iterates over all the offers which is assigned to one seller and n buyers.
        For each offer, the buyers speak, then the seller of the offer speaks.
        Every agent makes a price for the offer and can update or not his limit price.
        The current and previous price are stored in the offer object.

        If a deal happens, the offer is closed with the deal attribute switching to True,
        and the buyer is removed from all the other offers.
        """
        round = 0
        print("\n")
        while round <= self.nb_rounds:
            print("====" * 4 + f" ROUND {round} " + "====" * 4)
            for offre in self.liste_offres:
                if not offre.deal:
                    for negociateur_id in offre.buyers_id_list:
                        negociateur = self.buyers_list[negociateur_id]
                        nouveau_prix = offre.price_list[negociateur_id]
                        prix_offre, deal = negociateur.run(
                            round, offre.seller_id, nouveau_prix
                        )
                        offre.update(negociateur_id, prix_offre, deal)

                        if deal:
                            self.sellers_list[offre.seller_id].deal = True
                            self.remove_buyer_from_offer(negociateur_id)
                            self.metrics.sellers_nb_rounds_before_deal[
                                str(negociateur_id)
                            ].append(round)
                            self.metrics.buyers_nb_rounds_before_deal[
                                str(offre.seller_id)
                            ].append(round)
                            self.metrics.deals["strategies"].append(
                                negociateur.strategy
                            )
                            self.metrics.deals["strategies"].append(
                                self.sellers_list[offre.seller_id].strategy
                            )
                            self.metrics.deals["couples"].append(
                                (negociateur_id, offre.seller_id)
                            )
                            break

                        # Metrics update
                        self.metrics.buyers_offers[str(negociateur_id)].append(
                            prix_offre
                        )
                        self.metrics.buyers_limit_prices[str(negociateur_id)].append(
                            negociateur.limit_price_list[offre.id]
                        )

                        print(
                            f"B{negociateur.id} offers {prix_offre:.2f} to S{offre.seller_id}"
                        )
                        fournisseur = self.sellers_list[offre.seller_id]
                        nouveau_prix = offre.price_list[negociateur_id]
                        prix_offre, deal = fournisseur.run(
                            round, negociateur_id, nouveau_prix
                        )
                        offre.update(negociateur_id, prix_offre, deal)

                        # Metrics update
                        self.metrics.sellers_offers[str(offre.seller_id)].append(
                            prix_offre
                        )
                        self.metrics.sellers_limit_prices[str(offre.seller_id)].append(
                            fournisseur.limit_price_list[offre.id]
                        )

                        if deal:
                            self.buyers_list[negociateur_id].deal = True
                            self.remove_buyer_from_offer(negociateur_id)
                            self.metrics.sellers_nb_rounds_before_deal[
                                str(negociateur_id)
                            ].append(round)
                            self.metrics.buyers_nb_rounds_before_deal[
                                str(offre.seller_id)
                            ].append(round)
                            self.metrics.deals["strategies"].append(
                                negociateur.strategy
                            )
                            self.metrics.deals["strategies"].append(
                                self.sellers_list[offre.seller_id].strategy
                            )
                            self.metrics.deals["couples"].append(
                                (negociateur_id, offre.seller_id)
                            )
                            break
                        print(
                            f"S{fournisseur.id} offers {prix_offre:.2f} to B{negociateur_id}"
                        )
                        print("\n")
            round += 1

    def env_metrics(self):
        return self.metrics
