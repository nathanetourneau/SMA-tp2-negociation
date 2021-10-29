import random
from agent import Seller, Buyer, SellerRandom, BuyerRandom
from offre import Offre
from strategies import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Environment:
    def __init__(
        self,
        nb_sellers,
        nb_buyers,
        nb_rounds,
        strategy,
        sellers_dict_list=None,  # List of dicts
        buyers_dict_list=None,  # List of dicts
    ):
        self.nb_rounds = nb_rounds
        if strategy == "complex":
            if sellers_dict_list and buyers_dict_list:
                self.sellers_list = []
                self.buyers_list = []
                for id, seller_dict in enumerate(sellers_dict_list):
                    self.sellers_list.append(
                        Seller(
                            id,
                            seller_dict["behavior"],
                            nb_buyers,
                            seller_dict["limit_price"],
                            seller_dict["nb_max_offers"],
                        )
                    )
                for id, buyer_dict in enumerate(buyers_dict_list):
                    self.buyers_list.append(
                        Buyer(
                            id,
                            buyer_dict["behavior"],
                            nb_sellers,
                            buyer_dict["limit_price"],
                            buyer_dict["nb_max_offers"],
                        )
                    )
            else:
                behavior = "modere"
                min_price = random.randrange(100, 150)
                max_price = random.randrange(50, 100)
                nb_max_offers = random.randint(nb_rounds // 2, nb_rounds)
                self.sellers_list = [
                    Seller(
                        i,
                        behavior,
                        nb_buyers,
                        min_price,
                        nb_max_offers,
                    )
                    for i in range(nb_sellers)
                ]
                self.buyers_list = [
                    Buyer(i, behavior, nb_sellers, max_price, nb_max_offers)
                    for i in range(nb_buyers)
                ]

        elif strategy == "random":
            min_price = random.randrange(90, 100)
            max_price = random.randrange(90, 100)
            nb_max_offers = random.randint(nb_rounds // 2, nb_rounds)
            self.sellers_list = [
                SellerRandom(i, nb_buyers, random.randint(90, 100), nb_max_offers)
                for i in range(nb_sellers)
            ]
            self.buyers_list = [
                BuyerRandom(i, nb_sellers, random.randint(90, 100), nb_max_offers)
                for i in range(nb_buyers)
            ]

        self.liste_offres = []
        c = 0
        for i in range(nb_sellers):
            self.liste_offres.append(Offre(c, i, [k for k in range(nb_buyers)]))
            c += 1

    def remove_negociateur(self, negociateur_id):
        for offre in self.liste_offres:
            offre.liste_negociateur_id.remove(negociateur_id)

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

        for round in range(self.nb_rounds):
            print(f"---------- ROUND {round} ----------")
            for offre in self.liste_offres:
                if not offre.deal:
                    for negociateur_id in offre.liste_negociateur_id:
                        negociateur = self.buyers_list[negociateur_id]
                        nouveau_prix = offre.liste_prix[negociateur_id]
                        prix_offre, deal = negociateur.run(
                            round, offre.fournisseur_id, nouveau_prix
                        )
                        offre.update(negociateur_id, prix_offre, deal)
                        if deal:
                            self.sellers_list[offre.fournisseur_id].deal = True
                            self.remove_negociateur(negociateur_id)
                            break
                        logger.debug(
                            f"N{negociateur.id} a proposé {prix_offre} pour F{offre.fournisseur_id}"
                        )
                        fournisseur = self.sellers_list[offre.fournisseur_id]
                        nouveau_prix = offre.liste_prix[negociateur_id]
                        prix_offre, deal = fournisseur.run(
                            round, negociateur_id, nouveau_prix
                        )
                        offre.update(negociateur_id, prix_offre, deal)
                        if deal:
                            self.buyers_list[negociateur_id].deal = True
                            self.remove_negociateur(negociateur_id)
                            break
                        logger.debug(
                            f"F{fournisseur.id} a proposé {prix_offre} pour N{negociateur_id}"
                        )
                        logger.debug("\n")
