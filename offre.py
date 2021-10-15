class Offre:
    def __init__(self, id, negociateur_id, fournisseur_id, prix):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.negociateur_id = negociateur_id
        self.prix = prix
        self.ancien_prix = None
        self.deal = False

    def update(self, nouveau_prix: float, deal: bool):
        self.prix = nouveau_prix
        self.deal = deal
