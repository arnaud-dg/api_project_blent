from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

######################################################################
######  Création des différentes classes de la Base de Données  ######
######################################################################

class Utilisateur(db.Model):
    __tablename__ = "Utilisateur"
    """ 
        Classe définissant la table des utilisateurs.
        Dénomination de l'objet dans les logs par le nom utilisateur.
        L'email et le mot de passe servent à l'authentification.
        Le rôle délimite les autorisation d'accès aux différentes fonctions.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # client ou admin | enum ?
    date_creation = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.nom}>"

class Produit(db.Model):
    __tablename__ = "Produit"
    """
        Classe définissant la table des produits.
        Dénomination de l'objet dans les logs par le nom produit.
        La description détaillée est facultative.
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    categorie = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, nullable=False, default=1)
    date_creation = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Produit {self.nom}>"


class Commande(db.Model):
    __tablename__ = "Commande"
    """ 
        Classe définissant la table des commandes.
        Dénomination de l'objet dans les logs par l'id de la commande.
        Une Commande est liée à un Utilisateur via la ForeignKey "utilisateur_id".
    """

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("Utilisateur.id"), nullable=False
    )
    date_commande = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    adresse_livraison = db.Column(db.String(100), nullable=False)
    statut = db.Column(
        db.String(20), nullable=False
    )  # en_attente, validée, expédiée, annulée | enum

    # Utilisateur.commandes  # → backref renvoie la liste des commandes
    user = db.relationship("Utilisateur", backref="commandes", lazy=True) 

    def __repr__(self):
        return f"<Commande {self.id}>"


class LigneCommande(db.Model):
    __tablename__ = "LigneCommande"
    """ 
        Classe définissant la table des commandes.
        Dénomination de l'objet dans les logs son id, le produit et la quantité.
        La ligne de commande sera supprimée si sa commande ou son produit sont supprimés.
    """

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(
        db.Integer, db.ForeignKey("Commande.id", ondelete="CASCADE"), nullable=False
    )
    produit_id = db.Column(
        db.Integer, db.ForeignKey("Produit.id", ondelete="CASCADE"), nullable=False
    )
    quantite = db.Column(db.Integer, nullable=False, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False)

    command = db.relationship("Commande", backref="lignes_commandes", lazy=True)
    product = db.relationship(
        "Produit",
        backref=db.backref("lignes_commandes", cascade="all, delete-orphan"),
        lazy=True,
    )

    @property
    def prix_total(self):
        return self.quantite * self.prix_unitaire

    def __repr__(self):
        return (
            f"<Ligne {self.id}, Produit: {self.produit_id}, Quantité: {self.quantite}>"
        )
