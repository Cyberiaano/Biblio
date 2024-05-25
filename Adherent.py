class Adherent:
    def __init__(self, idAdherent, nom, prenom, gmail,adress, telephone):
        self.idAdherent = idAdherent
        self.nom = nom
        self.prenom = prenom
        self.gmail = gmail
        self.telephone = telephone
        self.adress = adress
    def ajouterAdherent(idAdherent, nom, prenom, gmail, telephone,address):
        return "adherent is added"
    def supprimerAdherent(idAdherent):
        return "adherent is deleted"
    def modifierAdherent(idAdherent, nom, prenom, gmail,adress, telephone):
        return "adherent is modified"
    def afficherAdherent(idAdherent):
        return "adherent is displayed"
    