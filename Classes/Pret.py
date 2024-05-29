class pret:
    def __init__(self, idPret, livre, adherent, datePret, dateRetour, etat, prix) :
        self.idPret = idPret
        self.livre = livre
        self.adherent = adherent
        self.datePret = datePret
        self.dateRetour = dateRetour
        self.etat = etat
        self.prix = prix
    def ajouterPret(idPret, livre, adherent, datePret, dateRetour, etat, prix):
        return "pret is added"
    def supprimerPret(idPret):
        return "pret is deleted"
    def modifierPret(idPret, livre, adherent, datePret, dateRetour, etat, prix):
        return "pret is modified"
    def afficherPret(idPret):
        return "pret is displayed"
    def afficherPretsParAdherent(idAdherent):
        return "prets are displayed"
