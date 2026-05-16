from datetime import datetime, timezone
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from src.models import LigneCommande, Produit, db
from src.utils import (
    check_fields,
    produit_to_dict,
    require_admin_authentication,
    require_authentication,
)

# Définition du blueprint product
product_bp = Blueprint("product_bp", __name__, url_prefix="/api/produits")

# Affichage de la liste des produits
@product_bp.route("", methods=["GET"])
@require_authentication
@swag_from("../swagger/products/list.yml")
def show_product_list():
    produits = Produit.query.all()
    items = [produit_to_dict(produit) for produit in produits]
    return jsonify(items), 200

# Affichage d'un produit en particulier
@product_bp.route("/<int:id>", methods=["GET"])
@require_authentication
@swag_from("../swagger/products/get_one.yml")
def show_one_product(id):
    produit = Produit.query.filter_by(id=id).first()

    # Vérif : Le produit existe dans la base
    if not produit:
        return jsonify({"error": "Produit non existant dans la base"}), 404

    return jsonify(produit_to_dict(produit)), 200

# Recherche d'un produit sur son nom ou sa catégorie
@product_bp.route("/search", methods=["GET"])
@require_authentication
@swag_from("../swagger/products/search.yml")
def search_products():
    nom = request.args.get("nom")
    categorie = request.args.get("categorie")

    query = Produit.query

    if nom:
        query = query.filter(Produit.nom.ilike(f"%{nom}%"))
    if categorie:
        query = query.filter(Produit.categorie.ilike(f"%{categorie}%"))

    produits = query.all()

    if not produits:
        return (
            jsonify(
                {"message": "Aucun produit ne correspond aux critères de recherche."}
            ),
            404,
        )

    items = [produit_to_dict(produit) for produit in produits]
    return jsonify(items), 200

# Création d'un produit
@product_bp.route("", methods=["POST"])
@require_admin_authentication
@swag_from("../swagger/products/create.yml")
def create_product():
    body = request.get_json()

    # Vérif : Présence de toutes les informations importantes
    if not check_fields(body, {"nom", "categorie", "prix", "quantite_stock"}):
        msg = (
            "Il manque a minima une information requise"
            " dans la requête. Vérifiez la saisie."
        )
        return jsonify({"error": msg}), 400

    existing_product = Produit.query.filter_by(nom=body["nom"]).first()
    # Vérif : Que le produit n'existe pas déjà
    if existing_product:
        msg = "Le produit que vous voulez créer existe déjà dans la base."
        return jsonify({"error": msg}), 400

    # Vérif : Format du prix et de la quantité cohérents
    try:
        prix = float(body["prix"])
        quantite_stock = int(body["quantite_stock"])
    except (ValueError, TypeError):
        msg = "Certains champs sont au mauvais format. Vérifiez votre saisie."
        return jsonify({"error": msg}), 400

    # Ajout du produit à la base de donnée avec la Class Produit
    new_product = Produit(
        nom=body["nom"],
        description=body.get("description", ""),
        categorie=body["categorie"],
        prix=prix,
        quantite_stock=quantite_stock,
        date_creation=datetime.now(timezone.utc),
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Produit ajouté à la base de donnée."}), 201

# Modification d'un produit
@product_bp.route("/<int:id>", methods=["PUT"])
@require_admin_authentication
@swag_from("../swagger/products/update.yml")
def modify_product(id):
    body = request.get_json()

    # Vérif : L'ensemble des champs requis sont présents
    if not check_fields(body, {"nom", "categorie", "prix", "quantite_stock"}):
        msg = (
            "Il manque a minima une information requise"
            " dans la requête. Vérifiez la saisie."
        )
        return jsonify({"error": msg}), 400

    existing_product = Produit.query.filter_by(id=id).first()
    # vérif : le produit existe dans la base
    if existing_product is None:
        msg = "Le produit que vous voulez modifier n'existe pas dans la base."
        return jsonify({"error": msg}), 404

    # Vérif : Format du prix et de la quantité cohérents
    try:
        prix = float(body["prix"])
        quantite_stock = int(body["quantite_stock"])
    except (ValueError, TypeError):
        msg = "Certains champs sont au mauvais format. Vérifiez votre saisie."
        return jsonify({"error": msg}), 400

    # Mise à jour des informations
    existing_product.nom = body["nom"]
    existing_product.description = body.get("description", "")
    existing_product.categorie = body["categorie"]
    existing_product.prix = prix
    existing_product.quantite_stock = quantite_stock

    db.session.commit()

    return jsonify({"message": "Produit modifié dans la base de donnée."}), 200

# Suppression d'un produit
@product_bp.route("/<int:id>", methods=["DELETE"])
@require_admin_authentication
@swag_from("../swagger/products/delete.yml")
def delete_product(id):
    existing_product = Produit.query.filter_by(id=id).first()
    # Vérif : Le produit existe dans la base
    if existing_product is None:
        msg = "Le produit que vous voulez supprimer n'existe pas dans la base."
        return jsonify({"error": msg}), 404

    command_on_going = LigneCommande.query.filter_by(produit_id=id).first()
    # Vérif : Le produit est attaché à des commandes en cours.
    if command_on_going:
        msg = (
            "Vous ne pouvez supprimer ce produit."
            " Il est actuellement en cours de commande."
        )
        return jsonify({"error": msg}), 400
    db.session.delete(existing_product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé de la base de donnée."}), 200
