class Fournisseur:
    def __init__(self, offre: dict, prix_min, taux_decroissance):
        self.type = offre["type"]
        self.date_max = offre["date_max_vente"]
        self.date_depart = offre["date_depart"]
        self.lieu_depart = offre["lieu_depart"]
        self.lieu_arrivee = offre["lieu_arrivee"]
        self.prix_min = prix_min
        self.taux_decroissance = taux_decroissance

    def is_satisfied(self, prix):
        return self.prix_min < prix

    def baisse_exigence(self):
        self.prix_min *= 1 - self.taux_decroissance


class Negociateur:
    def __init__(self, demande: dict, prix_max, nb_offres_max, taux_croissance):
        self.type = demande["type"]
        self.prix = demande["prix"]
        self.date_max = demande["date_max_vente"]
        self.date_depart = demande["date_depart"]
        self.lieu_depart = demande["lieu_depart"]
        self.lieu_arrivee = demande["lieu_arrivee"]
        self.prix_max = prix_max
        self.nb_offres_max = nb_offres_max
        self.taux_croissance = taux_croissance
        self.nb_offres = 0

    def is_satisfied(self):
        return self.prix <= self.prix_max

    def new_offre(self):
        self.prix *= 1 + self.taux_croissance
        self.nb_offres += 1
        return self.prix

    def imbroglio(self):
        return self.nb_offres >= self.nb_offres_max


def main():
    negociateur = Negociateur(
        {
            "type": "avion",
            "prix": 630,
            "date_max_vente": "25/12",
            "date_depart": "01/01",
            "lieu_depart": "Limoges",
            "lieu_arrivee": "San Francisco",
        },
        prix_max=800,
        nb_offres_max=5,
        taux_croissance=0.1,
    )
    fournisseur = Fournisseur(
        {
            "type": "avion",
            "date_max_vente": "25/12",
            "date_depart": "01/01",
            "lieu_depart": "Limoges",
            "lieu_arrivee": "San Francisco",
        },
        prix_min=800,
        taux_decroissance=0.1,
    )

    nb_rounds = 10

    for round in range(nb_rounds):
        if negociateur.imbroglio():
            return f"Echec de la négociation : {negociateur.nb_offres} offres effectuées, sans accord, nb_rounds =  {round}"

        if fournisseur.is_satisfied(negociateur.prix) and negociateur.is_satisfied():
            return f"Everyone is satisfied with price {negociateur.prix}, nb_rounds =  {round}"

        negociateur.new_offre()
        fournisseur.baisse_exigence()


if __name__ == "__main__":
    rv = main()
    print(rv)
