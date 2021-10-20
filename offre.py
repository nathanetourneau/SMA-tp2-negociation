class Offre:
    def __init__(self, id, fournisseur_id, negociateur_id, prix=None):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.negociateur_id = negociateur_id
        self.prix = prix
        self.ancien_prix = None

    def update(self, nouveau_prix: float):
        self.ancien_prix = self.prix
        self.prix = nouveau_prix
