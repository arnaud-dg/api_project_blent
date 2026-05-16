"""
Configuration partagée pour la suite de tests pytest.

Ce fichier est chargé automatiquement par pytest. Il définit les fixtures
disponibles dans tous les fichiers de test, ainsi que la fonction utilitaire
make_token pour générer des JWT sans passer par la route /login.
"""

import os

import jwt
import pytest
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from src.app import app as flask_app
from src.models import Produit, Utilisateur
from src.models import db as _db

load_dotenv()


@pytest.fixture(scope="session")
def app():
    """Configure et retourne l'application Flask en mode test.

    Utilise une base SQLite en mémoire pour isoler les tests de la base
    réelle. Portée session : une seule instance pour toute la session de tests.
    """
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return flask_app

@pytest.fixture(scope="function")
def client(app):
    """Fournit un client HTTP de test avec une base de données vierge.

    Crée toutes les tables avant chaque test et les supprime après,
    garantissant une isolation complète entre les tests.
    """
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def admin_user(app):
    """Insère un utilisateur admin en base et retourne ses infos (id, email, role).

    Utilisé pour tester les routes réservées aux administrateurs.
    """
    with app.app_context():
        user = Utilisateur(
            email="admin@test.fr",
            mot_de_passe=generate_password_hash("Admin1!"),
            nom="Admin Test",
            role="admin",
        )
        _db.session.add(user)
        _db.session.commit()
        _db.session.refresh(user)
        return user.id, user.email, user.role

@pytest.fixture
def client_user(app):
    """Insère un utilisateur client en base et retourne ses infos (id, email, role).

    Utilisé pour tester les routes accessibles aux utilisateurs standard.
    """
    with app.app_context():
        user = Utilisateur(
            email="client@test.fr",
            mot_de_passe=generate_password_hash("Client1!"),
            nom="Client Test",
            role="client",
        )
        _db.session.add(user)
        _db.session.commit()
        _db.session.refresh(user)
        return user.id, user.email, user.role

@pytest.fixture
def sample_product(app):
    """Insère un produit de référence en base et retourne ses infos.

    Retourne un tuple (id, nom, prix, quantite_stock) utilisable dans
    les tests de produits et de commandes.
    """
    with app.app_context():
        produit = Produit(
            nom="Doliprane 1000",
            description="Paracétamol 1000 mg",
            categorie="Médicament OTC",
            prix=2.49,
            quantite_stock=50,
        )
        _db.session.add(produit)
        _db.session.commit()
        _db.session.refresh(produit)
        return produit.id, produit.nom, produit.prix, produit.quantite_stock

def make_token(user_id, email, role):
    """Génère un token JWT signé pour un utilisateur de test.

    Forge le token directement avec la clé secrète de l'application,
    sans passer par la route /login, pour accélérer la mise en place des tests.
    """
    return jwt.encode(
        {"user_id": user_id, "email": email, "role": role},
        os.getenv("SECRET_JWT_TOKEN"),
        algorithm="HS256",
    )
