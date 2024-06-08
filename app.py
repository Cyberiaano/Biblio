from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from bson.errors import InvalidId
from neo4j import GraphDatabase

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.Bibliothèque
collection_livre = db.livres
collection_adherents = db.adherents
collection_prets = db.prets

# Connexion à Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gerer-livres')
def index():
    return render_template('gerer-livres.html')

@app.route('/gerer-prets')
def prets():
    # Récupérer tous les livres pour le formulaire de sélection de livre
    livres = list(collection_livre.find())
    return render_template('gerer-prets.html', livres=livres)

@app.route('/gerer_auteurs')
def auteurs():
    with driver.session() as session:
        result = session.run("MATCH (b:Auteur) RETURN b")
        auteurs = [record["b"] for record in result]
    return render_template('gerer-auteurs.html', auteurs=auteurs)
@app.route('/ajouter-auteur', methods=['POST'])
def ajouter_auteur():
    nom = request.form['nom']
    prenom = request.form['prenom']
    date_naissance = request.form['date_naissance']
    with driver.session() as session:
        session.run(
            "CREATE (a:Auteur {nom: $nom, prenom: $prenom, date_naissance: $date_naissance})",
            nom=nom, prenom=prenom, date_naissance=date_naissance
        )
    flash("Auteur ajouté avec succès!")
    return redirect(url_for('auteurs'))

@app.route('/supprimer-auteur/<id>', methods=['POST'])
def supprimer_auteur(id):
    with driver.session() as session:
        session.run("MATCH (a:Auteur) WHERE ID(a) = $id DELETE a", id=int(id))
    flash("Auteur supprimé avec succès!")
    return redirect(url_for('auteurs'))

@app.route('/gerer-utilisateurs', methods=['GET'])
def utilisateurs():
    with driver.session() as session:
        result = session.run("MATCH (u:Utilisateur) RETURN u")
        utilisateurs = [record["u"] for record in result]
    return render_template('gerer-utilisateurs.html', utilisateurs=utilisateurs)

@app.route('/ajouter-utilisateur', methods=['POST'])
def ajouter_utilisateur():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    password = request.form['password']
    with driver.session() as session:
        session.run(
            "CREATE (u:Utilisateur {nom: $nom, prenom: $prenom, email: $email, password: $password})",
            nom=nom, prenom=prenom, email=email, password=password
        )
    flash("Utilisateur ajouté avec succès!")
    return redirect(url_for('utilisateurs'))

@app.route('/supprimer-utilisateur/<id>', methods=['POST'])
def supprimer_utilisateur(id):
    with driver.session() as session:
        session.run("MATCH (u:Utilisateur) WHERE ID(u) = $id DELETE u", id=int(id))
    flash("Utilisateur supprimé avec succès!")
    return redirect(url_for('utilisateurs'))

@app.route('/search_book', methods=['GET'])
def search_book():
    query = request.args.get('query')
    if query:
        livres = list(collection_livre.find({"titre": {"$regex": query, "$options": "i"}}))
    else:
        livres = []
    return render_template('search_results.html', livres=livres, query=query)

def synchronize_book(book):
    with driver.session() as session:
        session.run("MERGE (b:Book {idLivre: $idLivre}) "
                    "SET b.titre = $titre, b.auteur = $auteur, b.dateEdition = $dateEdition, "
                    "b.genre = $genre, b.nbPages = $nbPages, b.resume = $resume",
                    idLivre=str(book['_id']), titre=book['titre'], auteur=book['auteur'],
                    dateEdition=book['date_edition'], genre=book['genre'],
                    nbPages=book['nb_pages'], resume=book['resume'])

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    date = request.form.get('date')
    genre = request.form.get('genre')
    nb_pages = request.form.get('nb_pages')
    resume = request.form.get('resume')

    livre = {
        "titre": title,
        "auteur": author,
        "date_edition": date,
        "genre": genre,
        "nb_pages": nb_pages,
        "resume": resume
    }

    result = collection_livre.insert_one(livre)
    if result.inserted_id:
        synchronize_book(livre)
        flash("Livre ajouté avec succès !", "success")
    else:
        flash("L'ajout du livre a échoué.", "error")
    return redirect(url_for('index'))

def synchronize_delete_book(book_id):
    with driver.session() as session:
        session.run("MATCH (b:Book {idLivre: $idLivre}) DETACH DELETE b",
                    idLivre=str(book_id))

@app.route('/delete_book/<id>', methods=['POST'])
def delete_book(id):
    result = collection_livre.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        synchronize_delete_book(id)  # Synchronize the deletion
        flash("Livre supprimé avec succès !", "success")
    else:
        flash("La suppression du livre a échoué.", "error")
    return redirect(url_for('search_book'))

@app.route('/user_loans/<cin>')
def user_loans(cin):
    user = collection_adherents.find_one({"cin": cin})
    if user:
        user['_id'] = str(user['_id'])
        prets = list(collection_prets.find({"IdAdherent": ObjectId(user['_id'])}))
        for pret in prets:
            pret['_id'] = str(pret['_id'])
            pret['IdLivre'] = str(pret['IdLivre'])
            pret['IdAdherent'] = str(pret['IdAdherent'])
            livre = collection_livre.find_one({"_id": ObjectId(pret['IdLivre'])})
            pret['LivreTitre'] = livre['titre'] if livre else 'Inconnu'
        livres = list(collection_livre.find())
        return render_template('user_loans.html', user=user, prets=prets, livres=livres)
    else:
        return render_template('add_user.html', cin=cin)

@app.route('/check_user', methods=['GET'])
def check_user():
    cin = request.args.get('cin')
    return redirect(url_for('user_loans', cin=cin))

@app.route('/add_loan', methods=['POST'])
def add_loan():
    user_id = request.form.get('user_id')
    cin = request.form.get('cin')

    try:
        # Vérifier si l'ID utilisateur est valide
        ObjectId(user_id)
    except InvalidId:
        # Si l'ID utilisateur n'est pas valide, renvoyer une erreur
        return jsonify({"success": False, "error": "ID utilisateur invalide"}), 400

    book_id = request.form.get('book')
    date_debut = datetime.now()
    date_fin = date_debut + timedelta(days=10)
    pret = {
        "IdLivre": ObjectId(book_id),
        "IdAdherent": ObjectId(user_id),
        "DateDeDebut": date_debut,
        "DateDeFin": date_fin,
        "Etat": "non rendu",
        "Prix": 10
    }
    result = collection_prets.insert_one(pret)
    if result.inserted_id:
        return redirect(url_for('user_loans', cin=cin))
    else:
        return jsonify({"success": False})

@app.route('/return_loan/<pret_id>', methods=['POST'])
def return_loan(pret_id):
    try:
        collection_prets.update_one({"_id": ObjectId(pret_id)}, {"$set": {"Etat": "rendu"}})
        flash("Prêt marqué comme rendu avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la mise à jour du prêt : {str(e)}", "error")
    return redirect(request.referrer)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = {
        "cin": request.form.get('cin'),
        "first_name": request.form.get('first-name'),
       
        "last_name": request.form.get('last-name'),
        "phone": request.form.get('phone'),
        "email": request.form.get('email')
    }
    result = collection_adherents.insert_one(user_data)
    if result.inserted_id:
        user_id = str(result.inserted_id)
        return redirect(url_for('user_loans', cin=user_data['cin']))
    else:
        flash("Échec de l'ajout de l'utilisateur.", "error")
        return redirect(url_for('prets'))

if __name__ == '__main__':
    app.run(debug=True)
