import logging
from connexion_db import driver
from Auteur import Auteur
logging.basicConfig(level=logging.INFO)

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
    @staticmethod
    def ajouterLivre(tx, idLivre, titre, auteur, dateEdition, genre, nbPages, resume):
        # Extraction de l'identifiant de l'auteur
        idAuteur = auteur.idAuteur
        
        # Vérifier si l'auteur existe déjà dans la base de données
        query_auteur_existe = (
            "MATCH (a:Auteur {idAuteur: $idAuteur}) "
            "RETURN a"
        )
        result_auteur = tx.run(query_auteur_existe, idAuteur=idAuteur)
        existing_author = result_auteur.single()

        if existing_author:
            # Si l'auteur existe, associer le livre à cet auteur
            query = (
                "MATCH (a:Auteur {idAuteur: $idAuteur}) "
                "CREATE (l:Livre {idLivre: $idLivre, titre: $titre, auteur: $idAuteur, "
                "dateEdition: $dateEdition, genre: $genre, nbPages: $nbPages, resume: $resume}) "
                "RETURN l"
            )
            result = tx.run(query, idLivre=idLivre, titre=titre, idAuteur=idAuteur,
                            dateEdition=dateEdition, genre=genre, nbPages=nbPages, resume=resume)
            return result.single()[0]
        else:
            # Si l'auteur n'existe pas, créer un nouvel auteur
            query_create_author = (
                "CREATE (a:Auteur {idAuteur: $idAuteur, nom: $nom, prenom: $prenom, "
                "gmail: $gmail, dateNaissance: $dateNaissance, dateDeces: $dateDeces}) "
                "RETURN a"
            )
            result_create_author = tx.run(query_create_author, idAuteur=idAuteur, nom=auteur.nom, prenom=auteur.prenom,
                                           gmail=auteur.gmail, dateNaissance=auteur.dateNaissance, dateDeces=auteur.dateDeces)
            # Associer le livre au nouvel auteur
            query = (
                "MATCH (a:Auteur {idAuteur: $idAuteur}) "
                "CREATE (l:Livre {idLivre: $idLivre, titre: $titre, auteur: $idAuteur, "
                "dateEdition: $dateEdition, genre: $genre, nbPages: $nbPages, resume: $resume}) "
                "RETURN l"
            )
            result = tx.run(query, idLivre=idLivre, titre=titre, idAuteur=idAuteur,
                            dateEdition=dateEdition, genre=genre, nbPages=nbPages, resume=resume)
            return result.single()[0]

    @staticmethod
    def supprimerLivre(tx, idLivre):
        query = (
            "MATCH (l:Livre {idLivre: $idLivre}) "
            "DELETE l"
        )
        tx.run(query, idLivre=idLivre)
        return "livre is deleted"

    @staticmethod
    def modifierLivre(tx, idLivre, titre, auteur, dateEdition, genre, nbPages, resume):
        # Extraction de l'identifiant de l'auteur
        idAuteur = auteur.idAuteur
        
        query = (
            "MATCH (l:Livre {idLivre: $idLivre}) "
            "SET l.titre = $titre, l.auteur = $idAuteur, l.dateEdition = $dateEdition, "
            "l.genre = $genre, l.nbPages = $nbPages, l.resume = $resume "
            "RETURN l"
        )
        result = tx.run(query, idLivre=idLivre, titre=titre, idAuteur=idAuteur, dateEdition=dateEdition,
                        genre=genre, nbPages=nbPages, resume=resume)
        return result.single()

    @staticmethod
    def afficherLivre(tx, idLivre):
        query = (
            "MATCH (l:Livre {idLivre: $idLivre}) "
            "RETURN l"
        )
        result = tx.run(query, idLivre=idLivre)
        return result.single()
    

class Session:
    def __init__(self, driver):
        self.driver = driver

    def execute_write(self, func, *args):
        with self.driver.session() as session:
            result = session.write_transaction(func, *args)
            return result

    def execute_read(self, func, *args):
        with self.driver.session() as session:
            result = session.read_transaction(func, *args)
            return result

# Just for testing if it works well, it would be removed in the final project
with driver.session() as session:
    created_author = session.execute_write(Auteur.ajouterAuteur, "12", "Johni", "Doe", "john.doe@gmail.com", "1995-01-01", None)
    print(f'Created author: {created_author}')

    created_book = session.execute_write(Livre.ajouterLivre, "100", "Titre du livre", Auteur("12", "Johni", "Doe", "john.doe@gmail.com", "1995-01-01", None), "2024-05-25", "Fiction", 200, "Résumé du livre")
    print(f'Created book: {created_book}')

    found_book = session.execute_read(Livre.afficherLivre, "100")
    print(f'Found book: {found_book}')

    updated_book = session.execute_write(Livre.modifierLivre, "100", "Nouveau titre", Auteur("12", "Johni", "Doe", "john.doe@gmail.com", "1995-01-01", None), "2024-05-25", "Fiction", 250, "Nouveau résumé")
    print(f'Updated book: {updated_book}')

    deletion_message = session.execute_write(Livre.supprimerLivre, "100")
    print(deletion_message)

driver.close()