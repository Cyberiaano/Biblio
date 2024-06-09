from pymongo import MongoClient
from neo4j import GraphDatabase

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.Bibliothèque
collection_livre = db.livres
collection_adherents = db.adherents
collection_prets = db.prets

# Connexion à Neo4j
username='neo4j'
password='youdourouch'
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(username, password))