class Metrics:
    def __init__(self, nb_sellers, nb_buyers):
        self.sellers_limit_prices = {}
        self.sellers_offers = {}
        self.sellers_nb_rounds_before_deal = {}
        self.buyers_limit_prices = {}
        self.buyers_offers = {}
        self.buyers_nb_rounds_before_deal = {}
        for seller_id in range(nb_sellers):
            self.sellers_limit_prices[str(seller_id)] = []
            self.sellers_offers[str(seller_id)] = []
            self.sellers_nb_rounds_before_deal[str(seller_id)] = []
        for buyer_id in range(nb_buyers):
            self.buyers_limit_prices[str(buyer_id)] = []
            self.buyers_offers[str(buyer_id)] = []
            self.buyers_nb_rounds_before_deal[str(buyer_id)] = []
