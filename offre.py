class Offre:
    def __init__(self, id, fournisseur_id, liste_negociateur_id, liste_prix=None):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.liste_negociateur_id = liste_negociateur_id
        if not liste_prix:
            self.liste_prix = [None for i in range(len(liste_negociateur_id))]
        else:
            self.liste_prix = liste_prix
        self.liste_ancien_prix = [None for i in range(len(liste_negociateur_id))]
        self.deal = False

    def update(self, negociateur_id, nouveau_prix: float, deal):
        self.liste_ancien_prix[negociateur_id] = self.liste_prix[negociateur_id]
        self.liste_prix[negociateur_id] = nouveau_prix
        self.deal = deal


# Il faut que les fournisseurs proposent les offres et que chaque offre ait un attribut liste_negociateurs.
# ça permet de fermer un offre lorsqu'il y a deal
