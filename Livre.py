class Livre:
    def __init__(self,idLivre, titre, auteur, dateEdition, genre, nbPages, resume):
        self.idLivre = idLivre
        self.titre = titre
        self.auteur = auteur
        self.dateEdition = dateEdition
        self.genre = genre
        self.nbPages = nbPages
        self.resume = resume
    def __str__(self):
        return "Livre: [idLivre: "+str(self.idLivre)+", titre: "+self.titre+", auteur: "+self.auteur+", dateEdition: "+self.dateEdition+", genre: "+self.genre+", nbPages: "+str(self.nbPages)+", resume: "+self.resume+"]"
    def ajouterLivres(idLivre, titre, auteur, dateEdition, genre, nbPages, resume):
        return "livre is added"
    def supprimerLivres(idLivre):
        return "livre is deleted"
    def modifierLivres(idLivre, titre, auteur, dateEdition, genre, nbPages, resume):
        return "livre is modified"
    def afficherLivres(idLivre):
        return "livre is displayed"

