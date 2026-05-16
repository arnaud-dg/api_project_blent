from datetime import datetime, timezone
from flasgger import swag_from
from flask import Blueprint, g, jsonify, request
from src.models import Commande, LigneCommande, Produit, db
from src.utils import (
    check_fields,
    commande_to_dict,
    ligne_commande_to_dict,
    require_admin_authentication,
    require_authentication,
)

# Définition du blueprint order
order_bp = Blueprint("order_bp", __name__, url_prefix="/api/commandes")

# Affichage des commandes 
# (uniquement les siennes pour user lambda | Toutes pour l'admin)
@order_bp.route("/", methods=["GET"])
@require_authentication
@swag_from("../swagger/orders/list.yml")
def show_commands():
    # Test sur le rôle lié au token JWT
    if g.user.get("role") == "admin":
        orders = Commande.query.all()
        items = [commande_to_dict(order) for order in orders]
    else:
        orders = Commande.query.filter_by(utilisateur_id=g.user.get("user_id")).all()
        items = [commande_to_dict(order) for order in orders]

    return jsonify(items), 200

# Affichage d'une commande particulière
# (uniquement les siennes pour user lambda | Toutes pour l'admin)
@order_bp.route("/<int:id>", methods=["GET"])
@require_authentication
@swag_from("../swagger/orders/get_one.yml")
def get_one_command(id):
    existing_order = Commande.query.filter_by(id=id).first()

    # Vérif : existance de la commande
    if existing_order is None:
        msg = "La commande que vous voulez visualiser n'existe pas dans la base."
        return jsonify({"error": msg}), 404

    # Vérif : droit d'accès, il faut que la commande appartienne à l'utilisateur
    if g.user.get("role") != "admin" and existing_order.utilisateur_id != g.user.get(
        "user_id"
    ):
        return (
            jsonify({"error": "Vous n'êtes pas autorisé à consulter cette commande."}),
            403,
        )

    return jsonify(commande_to_dict(existing_order)), 200

# Création d'une commande
@order_bp.route("", methods=["POST"])
@require_authentication
@swag_from("../swagger/orders/create.yml")
def create_command():
    body = request.get_json()

    # Vérif : Présence de tous les champs impératifs
    if not check_fields(body, {"adresse_livraison", "produits_commandes"}):
        msg = "Il manque des informations requises dans la requête."
        return jsonify({"error": msg}), 400

    adresse_livraison = body.get("adresse_livraison")
    produits_commandes = body.get("produits_commandes")

    # Vérif : Les champs non nullables ne doivent pas être vides
    if not isinstance(adresse_livraison, str) or not adresse_livraison.strip():
        msg = "L'adresse de livraison doit être une chaîne de caractères non vide."
        return jsonify({"error": msg}), 400
    if not isinstance(produits_commandes, list) or len(produits_commandes) == 0:
        msg = "La liste des produits commandés doit être une liste non vide."
        return jsonify({"error": msg}), 400

    lignes_preparees = []

    # Création des lignes de commande
    for index, ligne in enumerate(produits_commandes, start=1):
        if not isinstance(ligne, dict):
            return jsonify({"error": f"La ligne {index} est invalide."}), 400

        # Vérif : Présence de tous les champs lignes impératifs
        if not check_fields(ligne, {"produit_id", "quantite"}):
            msg = f"La ligne {index} doit contenir 'produit_id' et 'quantite'."
            return jsonify({"error": msg}), 400

        produit_id = ligne.get("produit_id")
        quantite = ligne.get("quantite")

        # Vérif : le champ produit doit être un entier
        if not isinstance(produit_id, int):
            msg = f"Le champ 'produit_id' de la ligne {index} doit être un entier."
            return jsonify({"error": msg}), 400

        # Vérif : Quantité positive
        if not isinstance(quantite, int) or quantite <= 0:
            msg = (
                f"Le champ 'quantite' de la ligne {index}"
                " doit être un entier strictement positif."
            )
            return jsonify({"error": msg}), 400

        # Vérif : le produit doit exister
        produit = Produit.query.filter_by(id=produit_id).first()
        if produit is None:
            return (
                jsonify({"error": f"Le produit d'id {produit_id} n'existe pas."}),
                404,
            )

        # Vérif : la quantité commandée ne peut être supérieure au stock
        if produit.quantite_stock < quantite:
            msg = (
                f"Stock insuffisant pour le produit '{produit.nom}'."
                f" Stock disponible : {produit.quantite_stock}."
            )
            return jsonify({"error": msg}), 400

        # Si tout est ok, ajout de la ligne
        lignes_preparees.append(
            {"produit": produit, "quantite": quantite, "prix_unitaire": produit.prix}
        )

    # Si tout est ok, création de la commande avec Class Commande
    new_order = Commande(
        utilisateur_id=g.user.get("user_id"),
        adresse_livraison=adresse_livraison.strip(),
        statut="en_attente",
        date_commande=datetime.now(timezone.utc),
    )

    db.session.add(new_order)
    db.session.flush()
    created_lines = []

    # Si tout est ok, création des lignes avec Class LigneCommande
    for ligne in lignes_preparees:
        produit = ligne["produit"]
        quantite = ligne["quantite"]
        prix_unitaire = ligne["prix_unitaire"]

        new_line = LigneCommande(
            commande_id=new_order.id,
            produit_id=produit.id,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
        )
        db.session.add(new_line)
        created_lines.append(new_line)

        # Mise à jour des quantités visibles pour les autres users
        produit.quantite_stock -= quantite

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Commande créée avec succès.",
                "commande": commande_to_dict(new_order),
                "lignes": [ligne_commande_to_dict(line) for line in created_lines],
            }
        ),
        201,
    )


# Mise à jour du statut d'une commande
@order_bp.route("/<int:id>", methods=["PATCH"])
@require_admin_authentication
@swag_from("../swagger/orders/update_status.yml")
def modify_command_status(id):
    body = request.get_json()

    # vérif : présence du statut à faire évoluer
    if not check_fields(body, {"statut"}):
        msg = "Il manque le statut souhaité dans la requête. Vérifiez la saisie."
        return jsonify({"error": msg}), 400

    # vérif : le statut est bien dans enum
    if body.get("statut") not in ["en_attente", "validée", "expédiée", "annulée"]:
        return jsonify({"error": "Le statut ne correspond pas à l'attendu."}), 400

    existing_order = Commande.query.filter_by(id=id).first()
    # vérif : existance de la commande
    if existing_order is None:
        msg = "La commande que vous voulez modifier n'existe pas dans la base."
        return jsonify({"error": msg}), 404

    # vérif : le statut demandé est déjà le statut actif
    if body.get("statut") == existing_order.statut:
        return jsonify({"error": "Le statut demandé est déjà le statut actuel."}), 400

    ancien_statut = existing_order.statut
    nouveau_statut = body.get("statut")
    existing_order.statut = nouveau_statut

    # Restauration du stock si la commande passe à "annulée"
    if nouveau_statut == "annulée" and ancien_statut != "annulée":
        for ligne in existing_order.lignes_commandes:
            ligne.product.quantite_stock += ligne.quantite

    db.session.commit()

    return (
        jsonify({"message": "Statut de commande modifié dans la base de données."}),
        200,
    )


# Affichage du contenu d'une commande
@order_bp.route("/<int:id>/lignes", methods=["GET"])
@require_authentication
@swag_from("../swagger/orders/get_lines.yml")
def get_command_lines(id):
    existing_order = Commande.query.filter_by(id=id).first()

    # Vérif : Si la commande existe
    if existing_order is None:
        msg = "La commande que vous voulez visualiser n'existe pas dans la base."
        return jsonify({"error": msg}), 404

    # Vérif : un client ne peut consulter que ses propres commandes
    if g.user.get("role") != "admin" and existing_order.utilisateur_id != g.user.get("user_id"):
        return jsonify({"error": "Vous n'êtes pas autorisé à consulter cette commande."}), 403

    commandlines = LigneCommande.query.filter_by(commande_id=id).all()
    items = [ligne_commande_to_dict(line) for line in commandlines]

    return jsonify(items), 200
