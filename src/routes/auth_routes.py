import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import Utilisateur, db
from src.utils import check_fields, is_valid_email, is_valid_password

# Chargement des variables d'environnement
load_dotenv()

# Récupération des token JWT (user standard | admin)
JWT_SECRET = os.getenv("SECRET_JWT_TOKEN")
ADMIN_SECRET = os.getenv("ADMIN_SECRET_TOKEN")

# Définition du blueprint auth
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

# Fonction d'enregistrement Sign-up
@auth_bp.route("/register", methods=["POST"])
@swag_from("../swagger/auth/register.yml")
def register_user():
    body = request.get_json()

    # Vérif : absence d'info
    if not check_fields(body, {"email", "mot_de_passe", "nom"}):
        msg = "Il manque une information requise dans la requête. Vérifiez la saisie."
        return jsonify({"error": msg}), 400

    # Vérif : email non valide
    if not is_valid_email(body["email"]):
        return jsonify({"error": "Renseignez une adresse email valide."}), 400

    # Vérif : mdp non valide
    if not is_valid_password(body["mot_de_passe"]):
        msg = (
            "Renseignez un mdp sécurisé"
            " (au moins 1 majuscule, 1 chiffre, 1 caractère spécial.)"
        )
        return jsonify({"error": msg}), 400

    # Vérif : utilisateur déjà existant
    existing_user = Utilisateur.query.filter_by(email=body["email"]).first()
    if existing_user:
        msg = "Adresse email déjà associée à un compte. Merci de vous identifier."
        return jsonify({"error": msg}), 400

    # Si en argment est ajouté le token ADMIN_SECRET, le rôle d'administrateur est attribué
    role = "admin" if body.get("secret") == ADMIN_SECRET else "client"

    # Conversion du password en hash /!\ Sécurité /!\
    hashed_password = generate_password_hash(body["mot_de_passe"])

    # Création d'un nouvel utilisateur dans la base grâce à la class Utilisateur
    new_user = Utilisateur(
        email=body["email"],
        mot_de_passe=hashed_password,
        nom=body["nom"],
        role=role,
        date_creation=datetime.now(timezone.utc),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Compte utilisateur créé."}), 200


# Fonction de connexion Sign-in
@auth_bp.route("/login", methods=["POST"])
@swag_from("../swagger/auth/login.yml")
def login_user():
    body = request.get_json()

    # Vérif : absence d'info
    if not check_fields(body, {"email", "mot_de_passe"}):
        msg = "Il manque une information requise dans la requête. Vérifiez la saisie."
        return jsonify({"error": msg}), 400

    # Vérif : utilisateur non existant dans la base
    existing_user = Utilisateur.query.filter_by(email=body["email"]).first()
    if existing_user is None:
        return (
            jsonify(
                {"error": "Le compte utilisateur n'existe pas. Merci de vous inscrire."}
            ),
            400,
        )

    # Vérif : password non correspondant
    if not check_password_hash(existing_user.mot_de_passe, body.get("mot_de_passe")):
        return jsonify({"error": "Mot de passe invalide."}), 400

    # Création d'un token grâce à JWT encode qui définit le user et son rôle
    token = jwt.encode(
        {
            "user_id": existing_user.id,
            "email": existing_user.email,
            "role": existing_user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    return jsonify({"message": "Utilisateur connecté.", "token": token}), 200
