from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from bson.errors import InvalidId

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.Bibliothèque
collection_livre = db.livres
collection_adherents = db.adherents
collection_prets = db.prets

# Route pour la page d'accueil
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
# Route pour rechercher un livre
@app.route('/search_book', methods=['GET'])
def search_book():
    query = request.args.get('query')
    if query:
        livres = list(collection_livre.find({"titre": {"$regex": query, "$options": "i"}}))
    else:
        livres = []
    return render_template('search_results.html', livres=livres, query=query)

# Route pour ajouter un livre
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    date = request.form.get('date')
    livre = {
        "titre": title,
        "auteur": author,
        "date_edition": date
    }
    result = collection_livre.insert_one(livre)
    if result.inserted_id:
        flash("Livre ajouté avec succès !", "success")
    else:
        flash("L'ajout du livre a échoué.", "error")
    return redirect(url_for('index'))

# Route pour supprimer un livre
@app.route('/delete_book/<id>', methods=['POST'])
def delete_book(id):
    result = collection_livre.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
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
