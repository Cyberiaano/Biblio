from Livre import Livre

monLivre = Livre(1, "Le Petit Prince", "Antoine de Saint-Exupéry", "1943", "Conte philosophique", 93, "Le Petit Prince est une œuvre de langue française, la plus connue d'Antoine de Saint-Exupéry. Publié en 1943 à New York simultanément à sa traduction anglaise, c'est une œuvre poétique et philosophique sous l'apparence d'un conte pour enfants.")
#print(monLivre)
a = Livre.supprimerLivres(2)
print(a)