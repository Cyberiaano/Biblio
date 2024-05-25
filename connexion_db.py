#connecting to neo4j db
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "youdourouch"

driver = GraphDatabase.driver(uri, auth=(username, password))