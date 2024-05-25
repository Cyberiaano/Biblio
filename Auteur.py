class Auteur:
    def __init__(self, idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        self.idAuteur = idAuteur
        self.nom = nom
        self.prenom = prenom
        self.gmail = gmail
        self.dateNaissance = dateNaissance
        self.dateDeces = dateDeces
    def ajouterAuteur(idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        return "auteur is added"
    def supprimerAuteur(idAuteur):
        return "auteur is deleted"
    def modifierAuteur(idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        return "auteur is modified"
    def afficherAuteur(idAuteur):
        return "auteur is displayed"