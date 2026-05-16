import os
import re
import jwt

from functools import wraps
from dotenv import load_dotenv
from flask import request, jsonify, g

# Chargement des variables d'environnement
load_dotenv()

# Création du token JWT
JWT_SECRET = os.getenv("SECRET_JWT_TOKEN")

# =========================================================
# Fonction de validation
# =========================================================

def check_fields(data, required_fields):
    """Retourne True si tous les champs de required_fields sont présents dans data."""
    # si le body est vide
    if not data:
        return False
    return required_fields.issubset(data.keys())

def is_valid_email(email):
    """Retourne True si l'email correspond au format attendu (ex: user@domaine.fr)."""
    # regex email
    pattern_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern_email, email) is not None

def is_valid_password(password):
    """Retourne True si le mot de passe contient au moins 1 majuscule, 1 chiffre et 1 caractère spécial."""
    # regex mdp
    pattern_mdp = r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$"
    return re.match(pattern_mdp, password) is not None

# =========================================================
# Fonctions d'authentification JWT
# =========================================================


def decode_token(token):
    """Décode un token JWT et retourne le payload, ou None si expiré ou invalide."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("Jeton JWT expiré.")
        return None
    except jwt.InvalidTokenError:
        print("Jeton JWT invalide.")
        return None


def require_authentication(f):
    """Décorateur qui vérifie la présence d'un token JWT valide et expose le payload dans g.user."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Jeton d'accès manquant."}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Jeton d'accès invalide."}), 401

        g.user = payload
        return f(*args, **kwargs)

    return wrapper


def require_admin_authentication(f):
    """Décorateur qui vérifie le token JWT et exige que le rôle soit admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Jeton d'accès manquant."}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Jeton d'accès invalide."}), 401

        if payload.get("role") != "admin":
            return (
                jsonify({"error": "Fonctionnalité réservée aux administrateurs."}),
                403,
            )

        g.user = payload
        return f(*args, **kwargs)

    return wrapper


# =========================================================
# Fonction de sérialisation JSON
# =========================================================

def produit_to_dict(produit):
    """Sérialise un objet Produit en dictionnaire JSON-compatible."""
    return {
        "id": produit.id,
        "nom": produit.nom,
        "description": produit.description,
        "categorie": produit.categorie,
        "prix": float(produit.prix),
        "quantite_stock": produit.quantite_stock,
    }

def commande_to_dict(commande):
    """Sérialise un objet Commande en dictionnaire JSON-compatible."""
    return {
        "id": commande.id,
        "utilisateur_id": commande.utilisateur_id,
        "date_commande": commande.date_commande,
        "adresse_livraison": commande.adresse_livraison,
        "statut": commande.statut,
    }

def ligne_commande_to_dict(ligne_commande):
    """Sérialise un objet LigneCommande en dictionnaire JSON-compatible."""
    return {
        "id": ligne_commande.id,
        "commande_id": ligne_commande.commande_id,
        "produit_id": ligne_commande.produit_id,
        "quantite": ligne_commande.quantite,
        "prix_unitaire": float(ligne_commande.prix_unitaire),
    }
