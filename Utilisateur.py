class Utilisateur:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def ajouterUtilisateur(username,password):
        return "utilisateur is added"
    def supprimerUtilisateur(username):
        return "utilisateur is deleted"
    def modifierUtilisateur(username,password):
        return "utilisateur is modified"
    def afficherUtilisateur(username):
        return "utilisateur is displayed"
    def authentification(username,password):
        return "utilisateur is authenticated"
    def deconnexion(username):
        return "utilisateur is disconnected"
    def afficherUtilisateurs():
        return "utilisateurs are displayed"