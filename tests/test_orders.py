"""Tests des routes commandes et de l'impact sur le stock."""

from conftest import make_token
from src.models import Produit
from src.models import db as _db


class TestCreateOrder:
    """Vérifie la route POST /api/commandes (création d'une commande par un utilisateur client)."""

    # Test positif de création de commande
    def test_success(self, client, client_user, sample_product):
        """Une commande valide est créée avec succès ; la réponse contient commande et lignes (201)."""
        product_id = sample_product[0]
        token = make_token(*client_user)
        res = client.post(
            "/api/commandes",
            headers={"Authorization": token},
            json={
                "adresse_livraison": "12 rue de la Paix, 75001 Paris",
                "produits_commandes": [{"produit_id": product_id, "quantite": 1}],
            },
        )
        assert res.status_code == 201
        data = res.get_json()
        assert "commande" in data
        assert "lignes" in data

    # Test négatif de création de commande. Demande supérieure au stock
    def test_insufficient_stock(self, client, client_user, sample_product):
        """Commander une quantité supérieure au stock disponible retourne une erreur (400)."""
        product_id, _, _, stock = sample_product
        token = make_token(*client_user)
        res = client.post(
            "/api/commandes",
            headers={"Authorization": token},
            json={
                "adresse_livraison": "12 rue de la Paix",
                "produits_commandes": [{"produit_id": product_id, "quantite": stock + 999}],
            },
        )
        assert res.status_code == 400

    # test positif de décrémentation de la qté en stock après commande
    def test_stock_decremented_after_order(self, client, client_user, sample_product, app):
        """Après validation d'une commande, le stock du produit est bien décrémenté en base."""
        product_id, _, _, initial_stock = sample_product
        token = make_token(*client_user)
        client.post(
            "/api/commandes",
            headers={"Authorization": token},
            json={
                "adresse_livraison": "12 rue de la Paix",
                "produits_commandes": [{"produit_id": product_id, "quantite": 3}],
            },
        )
        with app.app_context():
            produit = _db.session.get(Produit, product_id)
            assert produit.quantite_stock == initial_stock - 3
