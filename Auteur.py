import logging
from connexion_db import driver

logging.basicConfig(level=logging.INFO)

class Auteur:
    def __init__(self, idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        self.idAuteur = idAuteur
        self.nom = nom
        self.prenom = prenom
        self.gmail = gmail
        self.dateNaissance = dateNaissance
        self.dateDeces = dateDeces
    
    @staticmethod
    def ajouterAuteur(tx, idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        query = (
            "CREATE (a:Auteur {idAuteur: $idAuteur, nom: $nom, prenom: $prenom, "
            "gmail: $gmail, dateNaissance: $dateNaissance, dateDeces: $dateDeces}) "
            "RETURN a"
        )
        result = tx.run(query, idAuteur=idAuteur, nom=nom, prenom=prenom, gmail=gmail, 
                        dateNaissance=dateNaissance, dateDeces=dateDeces)
        return result.single()[0]
    
    @staticmethod
    def supprimerAuteur(tx, idAuteur):
        query = (
            "MATCH (a:Auteur {idAuteur: $idAuteur}) "
            "DELETE a"
        )
        tx.run(query, idAuteur=idAuteur)
        return "auteur is deleted"
    
    @staticmethod
    def modifierAuteur(tx, idAuteur, nom, prenom, gmail, dateNaissance, dateDeces):
        query = (
            "MATCH (a:Auteur {idAuteur: $idAuteur}) "
            "SET a.nom = $nom, a.prenom = $prenom, a.gmail = $gmail, "
            "a.dateNaissance = $dateNaissance, a.dateDeces = $dateDeces "
            "RETURN a"
        )
        result = tx.run(query, idAuteur=idAuteur, nom=nom, prenom=prenom, gmail=gmail, 
                        dateNaissance=dateNaissance, dateDeces=dateDeces)
        return result.single()
    
    @staticmethod
    def afficherAuteur(tx, idAuteur):
        query = (
            "MATCH (a:Auteur {idAuteur: $idAuteur}) "
            "RETURN a"
        )
        result = tx.run(query, idAuteur=idAuteur)
        return result.single()


# just for testing if it work well, it would be removed in the final project
with driver.session() as session:
        created_person = session.execute_write(Auteur.ajouterAuteur, "1", "John", "Doe", "john.doe@gmail.com", "1995-01-01", None)
        print(f'Created person: {created_person}')

        found_person = session.execute_read(Auteur.afficherAuteur, "1")
        print(f'Found person: {found_person}')

        updated_person = session.execute_write(Auteur.modifierAuteur, "1", "John", "Doe", "john.doe_updated@gmail.com", "1995-01-01", None)
        print(f'Updated person: {updated_person}')

        deletion_message = session.execute_write(Auteur.supprimerAuteur, "1")
        print(deletion_message)

driver.close()
