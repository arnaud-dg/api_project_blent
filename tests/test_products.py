"""Tests des routes produits et du modèle Produit."""

from conftest import make_token
from src.models import Produit
from src.models import db as _db
from src.utils import produit_to_dict

PRODUCT_PAYLOAD = {
    "nom": "Ibuprofène 200",
    "categorie": "Médicament OTC",
    "prix": 3.95,
    "quantite_stock": 30,
}

class TestGetProducts:
    """Vérifie la route GET /api/produits (liste complète des produits)."""

    # Test positif affichage de la liste des produits
    def test_list_products(self, client, client_user):
        """Un utilisateur authentifié reçoit la liste des produits sous forme de tableau (200)."""
        token = make_token(*client_user)
        res = client.get("/api/produits", headers={"Authorization": token})
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

class TestGetOneProduct:
    """Vérifie la route GET /api/produits/<id> (détail d'un produit)."""

    # Test positif existence produit
    def test_existing_product(self, client, client_user, sample_product):
        """Un produit existant est retourné avec succès (200)."""
        product_id = sample_product[0]
        token = make_token(*client_user)
        res = client.get(f"/api/produits/{product_id}", headers={"Authorization": token})
        assert res.status_code == 200

    # test négatif existence produit
    def test_nonexistent_product(self, client, client_user):
        """Un identifiant inconnu retourne une erreur 404."""
        token = make_token(*client_user)
        res = client.get("/api/produits/9999", headers={"Authorization": token})
        assert res.status_code == 404

class TestCreateProduct:
    """Vérifie la route POST /api/produits (création d'un produit, réservée aux admins)."""

    # Test positif de création produit par admin
    def test_admin_can_create(self, client, admin_user):
        """Un admin peut créer un nouveau produit avec des données valides (201)."""
        token = make_token(*admin_user)
        res = client.post("/api/produits", headers={"Authorization": token}, json=PRODUCT_PAYLOAD)
        assert res.status_code == 201

    # Test négatif de création de produit - déjà existant
    def test_duplicate_name(self, client, admin_user, sample_product):
        """Tenter de créer un produit avec un nom déjà existant en base retourne une erreur (400)."""
        token = make_token(*admin_user)
        res = client.post(
            "/api/produits",
            headers={"Authorization": token},
            json={**PRODUCT_PAYLOAD, "nom": "Doliprane 1000"},
        )
        assert res.status_code == 400

class TestModifyProduct:
    """Vérifie les contrôles d'accès sur la route PUT /api/produits/<id>."""

    # test négatif de modification produit (non admin)
    def test_client_cannot_modify(self, client, client_user, sample_product):
        """Un utilisateur non-admin qui tente de modifier un produit est refusé (403)."""
        product_id = sample_product[0]
        token = make_token(*client_user)
        res = client.put(
            f"/api/produits/{product_id}",
            headers={"Authorization": token},
            json=PRODUCT_PAYLOAD,
        )
        assert res.status_code == 403

class TestProductModel:
    """Vérifie le modèle Produit en isolation, sans passer par les routes HTTP."""

    # Test positif attributs produit
    def test_product_attributes(self):
        """Un objet Produit instancié en mémoire possède bien les attributs fournis."""
        p = Produit(nom="Vitamine C", categorie="Complément", prix=4.99, quantite_stock=20)
        assert p.nom == "Vitamine C"
        assert p.prix == 4.99
        assert p.quantite_stock == 20
        assert p.categorie == "Complément"

    # Test positif sérialisation
    def test_product_serialization(self, client, app, sample_product):
        """produit_to_dict retourne un dictionnaire dont les valeurs correspondent au produit en base."""
        with app.app_context():
            produit = _db.session.get(Produit, sample_product[0])
            d = produit_to_dict(produit)
            assert d["nom"] == sample_product[1]
            assert d["prix"] == sample_product[2]
            assert d["quantite_stock"] == sample_product[3]
