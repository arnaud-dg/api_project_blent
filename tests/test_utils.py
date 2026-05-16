"""Tests unitaires des fonctions utilitaires : check_fields, is_valid_email, is_valid_password."""

from src.utils import check_fields, is_valid_email, is_valid_password


class TestCheckFields:
    """Vérifie que check_fields détecte correctement la présence des champs requis."""

    def test_all_fields_present(self):
        """Tous les champs requis sont présents dans le dictionnaire → retourne True."""
        assert check_fields({"a": 1, "b": 2}, {"a", "b"}) is True

    def test_empty_data(self):
        """Dictionnaire vide alors qu'un champ est requis → retourne False."""
        assert check_fields({}, {"a"}) is False


class TestIsValidEmail:
    """Vérifie que is_valid_email accepte les emails valides et rejette les malformés."""

    def test_valid_email(self):
        """Email au format standard valide → retourne True."""
        assert is_valid_email("user@example.com") is True

    def test_missing_domain(self):
        """Email sans domaine après le @ → retourne False."""
        assert is_valid_email("user@") is False


class TestIsValidPassword:
    """Vérifie que is_valid_password applique les règles de complexité du mot de passe."""

    def test_valid_password(self):
        """Mot de passe contenant majuscule, chiffre et caractère spécial → retourne True."""
        assert is_valid_password("Secure1!") is True

    def test_no_special_char(self):
        """Mot de passe sans caractère spécial → retourne False."""
        assert is_valid_password("Secure123") is False
