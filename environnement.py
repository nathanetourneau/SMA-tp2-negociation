class Environnement:
    def __init__(self):
        self.liste_fournisseurs = None
        self.liste_negociateurs = None
        self.liste_offres = None
        self.array_offres = None

    def remove_negociateur(self, negociateur_id):
        for offre in self.liste_offres:
            offre.liste_negociateur_id.remove(negociateur_id)
