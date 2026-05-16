"""Tests des routes d'authentification : inscription et connexion."""

class TestRegister:
    """Vérifie le comportement de la route POST /api/auth/register."""

    # Test positif enregistrement de client
    def test_success(self, client):
        """Un nouvel utilisateur avec des données valides est créé avec succès (200)."""
        res = client.post("/api/auth/register", json={
            "email": "new@test.fr",
            "mot_de_passe": "Secure1!",
            "nom": "Nouveau",
        })
        assert res.status_code == 200

class TestLogin:
    """Vérifie le comportement de la route POST /api/auth/login."""

    # Test positif connexion de client
    def test_success(self, client, client_user):
        """Un utilisateur existant avec les bons identifiants reçoit un token JWT (200)."""
        res = client.post("/api/auth/login", json={
            "email": "client@test.fr",
            "mot_de_passe": "Client1!",
        })
        assert res.status_code == 200
        assert "token" in res.get_json()

    # Test négatif connexion de client
    def test_wrong_password(self, client, client_user):
        """Un utilisateur existant avec un mauvais mot de passe est refusé (400)."""
        res = client.post("/api/auth/login", json={
            "email": "client@test.fr",
            "mot_de_passe": "Mauvais1!",
        })
        assert res.status_code == 400
        assert "token" not in res.get_json()
