-- =====================================================
-- ParaShop — schéma de la base de données
-- Source : src/models.py (SQLAlchemy)
-- Cible  : drawDB — dialecte PostgreSQL/SQLite générique
-- =====================================================

-- ---------- Table : Utilisateur ----------
CREATE TABLE Utilisateur (
    id              INTEGER       PRIMARY KEY,
    email           VARCHAR(100)  NOT NULL UNIQUE,
    mot_de_passe    VARCHAR(100)  NOT NULL,
    nom             VARCHAR(100)  NOT NULL,
    role            VARCHAR(20)   NOT NULL,
    date_creation   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Table : Produit ----------
CREATE TABLE Produit (
    id              INTEGER       PRIMARY KEY,
    nom             VARCHAR(100)  NOT NULL,
    description     TEXT,
    categorie       VARCHAR(100)  NOT NULL,
    prix            FLOAT         NOT NULL,
    quantite_stock  INTEGER       NOT NULL DEFAULT 1,
    date_creation   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Table : Commande ----------
CREATE TABLE Commande (
    id                  INTEGER       PRIMARY KEY,
    utilisateur_id      INTEGER       NOT NULL,
    date_commande       TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    adresse_livraison   VARCHAR(100)  NOT NULL,
    statut              VARCHAR(20)   NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
);

-- ---------- Table : LigneCommande ----------
CREATE TABLE LigneCommande (
    id              INTEGER  PRIMARY KEY,
    commande_id     INTEGER  NOT NULL,
    produit_id      INTEGER  NOT NULL,
    quantite        INTEGER  NOT NULL DEFAULT 1,
    prix_unitaire   FLOAT    NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES Commande(id) ON DELETE CASCADE,
    FOREIGN KEY (produit_id)  REFERENCES Produit(id)  ON DELETE CASCADE
);
