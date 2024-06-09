from connexion import driver

def synchronize_Ajout_book(book):
    with driver.session() as session:
        session.run(
            "MERGE (b:Book {idLivre: $idLivre}) "
            "SET b.titre = $titre, b.auteur = $auteur, b.dateEdition = $dateEdition, "
            "b.genre = $genre, b.nbPages = $nbPages, b.resume = $resume",
            idLivre=str(book['_id']), titre=book['titre'], auteur=book['auteur'],
            dateEdition=book['date_edition'], genre=book['genre'],
            nbPages=book['nb_pages'], resume=book['resume']
        )

def synchronize_delete_book(book_id):
    with driver.session() as session:
        session.run("MATCH (b:Book {idLivre: $idLivre}) DETACH DELETE b", idLivre=str(book_id))
