from flask import Flask
from routes import init_routes
from authentication import initialize_admin

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Initialiser les routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
    initialize_admin()
