from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from bson.errors import InvalidId
from neo4j import GraphDatabase
# Connexion à Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Ouverture de la session
with driver.session() as session:
    result = session.run("MATCH (u:Utilisateur) RETURN u")
    collection_utilisateurs = [record["u"] for record in result]
print(collection_utilisateurs)