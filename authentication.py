from connexion import driver
import bcrypt


def initialize_admin():
    with driver.session() as session:
        # Check if there are any users in the database
        result = session.run("MATCH (u:Utilisateur) RETURN COUNT(u) AS user_count")
        user_count = result.single()["user_count"]

        # If no users are found, create the initial admin user
        if user_count == 0:
            admin_username = "admin"
            admin_password = "admin"  # Change this to a more secure password
            admin_hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

            session.run(
                """
                CREATE (u:Utilisateur {nom: $nom, prenom: 'Admin', email: 'admin@example.com', password: $hashed_password, role: 'admin'})
                """,
                nom=admin_username, hashed_password=admin_hashed_password.decode('utf-8')
            )
            print("Initial admin user created with username: admin and password: admin")


