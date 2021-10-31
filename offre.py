class Offre:
    def __init__(self, id, seller_id, buyers_id_list, price_list=None):
        self.id = id
        self.seller_id = seller_id
        self.buyers_id_list = buyers_id_list
        if not price_list:
            self.price_list = [None for i in range(len(buyers_id_list))]
        else:
            self.price_list = price_list
        self.previous_price_list = [None for i in range(len(buyers_id_list))]
        self.deal = False

    def update(self, buyer_id, new_price: float, deal):
        self.previous_price_list[buyer_id] = self.price_list[buyer_id]
        self.price_list[buyer_id] = new_price
        self.deal = deal
