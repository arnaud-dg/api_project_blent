"""
Initialisation et Simulation de la base de données de l'application ParaShop.

Ce module fournit des fonctions utilitaires pour réinitialiser la base,
créer les tables et insérer des données de test (utilisateurs, produits,
commandes et lignes de commande). 
A exécuter manuellement en développement via `python -m src.db_init`.
"""

from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash # Bibliothèque de sécurité incluse avec Flask. evite le stockage en dur des mdp.
from src.app import app
from src.models import Commande, LigneCommande, Produit, Utilisateur, db

def reset_database():
    """Supprime toutes les tables existantes et les recrée à partir des modèles."""
    db.drop_all()
    db.create_all()


def seed_users():
    """Insère 10 utilisateurs de test : 2 admins et 8 clients. Retourne la liste des objets créés."""
    users = [
        Utilisateur(
            email="admin1@parashop.fr",
            mot_de_passe=generate_password_hash("Admin1!"),
            nom="Claire Martin",
            role="admin",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="admin2@parashop.fr",
            mot_de_passe=generate_password_hash("Admin2!"),
            nom="Thomas Bernard",
            role="admin",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="alice.dupont@test.fr",
            mot_de_passe=generate_password_hash("Client1!"),
            nom="Alice Dupont",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="marc.leroy@test.fr",
            mot_de_passe=generate_password_hash("Client2!"),
            nom="Marc Leroy",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="sophie.moreau@test.fr",
            mot_de_passe=generate_password_hash("Client3!"),
            nom="Sophie Moreau",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="julien.robert@test.fr",
            mot_de_passe=generate_password_hash("Client4!"),
            nom="Julien Robert",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="camille.petit@test.fr",
            mot_de_passe=generate_password_hash("Client5!"),
            nom="Camille Petit",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="nicolas.girard@test.fr",
            mot_de_passe=generate_password_hash("Client6!"),
            nom="Nicolas Girard",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="emma.roux@test.fr",
            mot_de_passe=generate_password_hash("Client7!"),
            nom="Emma Roux",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
        Utilisateur(
            email="lucas.fontaine@test.fr",
            mot_de_passe=generate_password_hash("Client8!"),
            nom="Lucas Fontaine",
            role="client",
            date_creation=datetime.now(timezone.utc),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()
    return users


def seed_products():
    """Insère 20 produits de test couvrant les catégories parapharmacie. Retourne la liste des objets créés."""
    products = [
        Produit(
            nom="Doliprane 1000 mg",
            description="Boîte de 8 comprimés de paracétamol pour douleurs et fièvre.",
            categorie="Médicament OTC",
            prix=2.49,
            quantite_stock=120,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Ibuprofène 200 mg",
            description="Anti-inflammatoire en comprimés, boîte de 20.",
            categorie="Médicament OTC",
            prix=3.95,
            quantite_stock=90,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Spray Nasal Eau de Mer",
            description="Spray pour lavage nasal quotidien.",
            categorie="Hygiène ORL",
            prix=5.80,
            quantite_stock=60,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Pastilles Gorge Miel Citron",
            description="Pastilles adoucissantes pour la gorge.",
            categorie="Médicament OTC",
            prix=4.20,
            quantite_stock=75,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Gel Hydroalcoolique 100 ml",
            description="Gel désinfectant pour les mains.",
            categorie="Hygiène",
            prix=2.99,
            quantite_stock=200,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Thermomètre Digital",
            description="Thermomètre électronique à affichage rapide.",
            categorie="Dispositif médical",
            prix=9.90,
            quantite_stock=35,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Vitamine C 1000",
            description="Complément alimentaire vitamine C, 30 comprimés.",
            categorie="Complément alimentaire",
            prix=6.50,
            quantite_stock=80,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Magnésium Marin",
            description="Complément alimentaire anti-fatigue, 60 gélules.",
            categorie="Complément alimentaire",
            prix=8.95,
            quantite_stock=70,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Crème Hydratante Visage",
            description="Crème visage peaux sensibles, 50 ml.",
            categorie="Parapharmacie",
            prix=11.90,
            quantite_stock=40,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Baume Lèvres Réparateur",
            description="Soin nourrissant et réparateur pour lèvres sèches.",
            categorie="Parapharmacie",
            prix=4.70,
            quantite_stock=55,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Crème Solaire SPF50+",
            description="Très haute protection solaire, 200 ml.",
            categorie="Parapharmacie",
            prix=14.50,
            quantite_stock=45,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Pansements Assortis",
            description="Boîte de 30 pansements multi-formats.",
            categorie="Premiers soins",
            prix=3.60,
            quantite_stock=100,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Solution Antiseptique",
            description="Solution antiseptique cutanée, 125 ml.",
            categorie="Premiers soins",
            prix=4.90,
            quantite_stock=65,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Sérum Physiologique",
            description="Unidoses pour hygiène du nez et des yeux.",
            categorie="Hygiène",
            prix=3.20,
            quantite_stock=110,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Sirop Toux Sèche",
            description="Sirop apaisant pour toux sèche, 150 ml.",
            categorie="Médicament OTC",
            prix=6.80,
            quantite_stock=50,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Gummies Sommeil Mélatonine",
            description="Complément alimentaire favorisant l'endormissement.",
            categorie="Complément alimentaire",
            prix=9.50,
            quantite_stock=60,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Shampoing Doux Dermatologique",
            description="Shampoing usage fréquent, peaux sensibles.",
            categorie="Parapharmacie",
            prix=7.90,
            quantite_stock=35,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Brosse à Dents Souple",
            description="Brosse à dents souple pour usage quotidien.",
            categorie="Hygiène bucco-dentaire",
            prix=2.80,
            quantite_stock=95,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Dentifrice Gencives Sensibles",
            description="Dentifrice protection gencives, 75 ml.",
            categorie="Hygiène bucco-dentaire",
            prix=4.10,
            quantite_stock=85,
            date_creation=datetime.now(timezone.utc),
        ),
        Produit(
            nom="Larmes Artificielles",
            description="Collyre lubrifiant pour yeux secs.",
            categorie="Ophtalmologie",
            prix=8.20,
            quantite_stock=30,
            date_creation=datetime.now(timezone.utc),
        ),
    ]

    db.session.add_all(products)
    db.session.commit()
    return products


def seed_orders(users, products):
    """
    Insère 5 commandes avec leurs lignes de commande pour 5 clients distincts.

    Args:
        users: liste des Utilisateur retournée par seed_users().
        products: liste des Produit retournée par seed_products().

    Returns:
        Tuple (orders, lines) contenant les listes des objets créés.
    """
    client_1 = users[2]
    client_2 = users[3]
    client_3 = users[4]
    client_4 = users[5]
    client_5 = users[6]

    orders = [
        Commande(
            utilisateur_id=client_1.id,
            adresse_livraison="12 rue Victor Hugo, 75011 Paris",
            statut="en_attente",
            date_commande=datetime.now(timezone.utc) - timedelta(days=5),
        ),
        Commande(
            utilisateur_id=client_2.id,
            adresse_livraison="8 avenue de la République, 69003 Lyon",
            statut="validée",
            date_commande=datetime.now(timezone.utc) - timedelta(days=4),
        ),
        Commande(
            utilisateur_id=client_3.id,
            adresse_livraison="25 boulevard Gambetta, 33000 Bordeaux",
            statut="expédiée",
            date_commande=datetime.now(timezone.utc) - timedelta(days=3),
        ),
        Commande(
            utilisateur_id=client_4.id,
            adresse_livraison="3 rue Nationale, 59000 Lille",
            statut="annulée",
            date_commande=datetime.now(timezone.utc) - timedelta(days=2),
        ),
        Commande(
            utilisateur_id=client_5.id,
            adresse_livraison="41 allée Jean Jaurès, 31000 Toulouse",
            statut="en_attente",
            date_commande=datetime.now(timezone.utc) - timedelta(days=1),
        ),
    ]

    db.session.add_all(orders)
    db.session.commit()

    lines = [
        # Commande 1
        LigneCommande(
            commande_id=orders[0].id,
            produit_id=products[0].id,
            quantite=2,
            prix_unitaire=products[0].prix,
        ),
        LigneCommande(
            commande_id=orders[0].id,
            produit_id=products[2].id,
            quantite=1,
            prix_unitaire=products[2].prix,
        ),
        LigneCommande(
            commande_id=orders[0].id,
            produit_id=products[11].id,
            quantite=3,
            prix_unitaire=products[11].prix,
        ),
        LigneCommande(
            commande_id=orders[0].id,
            produit_id=products[13].id,
            quantite=2,
            prix_unitaire=products[13].prix,
        ),
        # Commande 2
        LigneCommande(
            commande_id=orders[1].id,
            produit_id=products[5].id,
            quantite=1,
            prix_unitaire=products[5].prix,
        ),
        LigneCommande(
            commande_id=orders[1].id,
            produit_id=products[6].id,
            quantite=2,
            prix_unitaire=products[6].prix,
        ),
        LigneCommande(
            commande_id=orders[1].id,
            produit_id=products[8].id,
            quantite=1,
            prix_unitaire=products[8].prix,
        ),
        # Commande 3
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[1].id,
            quantite=1,
            prix_unitaire=products[1].prix,
        ),
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[3].id,
            quantite=2,
            prix_unitaire=products[3].prix,
        ),
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[9].id,
            quantite=2,
            prix_unitaire=products[9].prix,
        ),
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[14].id,
            quantite=1,
            prix_unitaire=products[14].prix,
        ),
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[16].id,
            quantite=1,
            prix_unitaire=products[16].prix,
        ),
        LigneCommande(
            commande_id=orders[2].id,
            produit_id=products[18].id,
            quantite=1,
            prix_unitaire=products[18].prix,
        ),
        # Commande 4
        LigneCommande(
            commande_id=orders[3].id,
            produit_id=products[4].id,
            quantite=4,
            prix_unitaire=products[4].prix,
        ),
        LigneCommande(
            commande_id=orders[3].id,
            produit_id=products[10].id,
            quantite=1,
            prix_unitaire=products[10].prix,
        ),
        LigneCommande(
            commande_id=orders[3].id,
            produit_id=products[17].id,
            quantite=2,
            prix_unitaire=products[17].prix,
        ),
        # Commande 5
        LigneCommande(
            commande_id=orders[4].id,
            produit_id=products[7].id,
            quantite=1,
            prix_unitaire=products[7].prix,
        ),
        LigneCommande(
            commande_id=orders[4].id,
            produit_id=products[12].id,
            quantite=1,
            prix_unitaire=products[12].prix,
        ),
        LigneCommande(
            commande_id=orders[4].id,
            produit_id=products[15].id,
            quantite=2,
            prix_unitaire=products[15].prix,
        ),
        LigneCommande(
            commande_id=orders[4].id,
            produit_id=products[19].id,
            quantite=1,
            prix_unitaire=products[19].prix,
        ),
    ]

    db.session.add_all(lines)
    db.session.commit()

    return orders, lines


def main():
    """Réinitialise la base et insère toutes les données de test. Affiche un résumé en console."""
    with app.app_context():
        reset_database() 
        users = seed_users()
        products = seed_products()
        orders, lines = seed_orders(users, products)

        print("Base réinitialisée")
        print(f"- Utilisateurs : {Utilisateur.query.count()}")
        print(f"- Produits : {Produit.query.count()}")
        print(f"- Commandes : {Commande.query.count()}")
        print(f"- Lignes de commande : {LigneCommande.query.count()}")


if __name__ == "__main__":
    main()
