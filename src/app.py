import os
from pathlib import Path

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask

from src.models import db
from src.routes.auth_routes import auth_bp
from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp

# Chargement des variables .env
load_dotenv()

app = Flask(__name__)

# Chemin absolu vers la base SQLite → src/data/parashop.db
# as_posix() force les forward slashes, obligatoires dans une URI SQLite sur Windows
_DB_PATH = (Path(__file__).resolve().parent / "data" / "parashop.db")
_DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # crée src/data/ si absent
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{_DB_PATH.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Définition des Blueprint Flask = Regroupement des routes
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)

# Correction des redirections derrière un reverse proxy (ex: Blent /proxy/5000)
# SCRIPT_NAME informe Flask du préfixe afin que les URLs générées l'incluent
_script_name = os.getenv("SCRIPT_NAME", "")
if _script_name:
    class _PrefixMiddleware:
        def __init__(self, wsgi_app, prefix):
            self.wsgi_app = wsgi_app
            self.prefix = prefix

        def __call__(self, environ, start_response):
            environ["SCRIPT_NAME"] = self.prefix
            return self.wsgi_app(environ, start_response)

    app.wsgi_app = _PrefixMiddleware(app.wsgi_app, _script_name)

# Implémentation d'un swagger pour améliorer la doc et la clarté utilisateur
swagger = Swagger(app, template={
    "info": {
        "title": "ParaShop API",
        "description": "API REST de la plateforme e-commerce ParaShop.",
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT sous la forme : Bearer <token>",
        }
    },
})

# Route d'acceuil
@app.route("/")
def welcome():
    return "Bienvenue sur le portail client de l'application e-commerce ParaShop"


if __name__ == "__main__":
    base_url = os.getenv("PUBLIC_URL", "http://127.0.0.1:5000")
    print(f" * API Docs  : {base_url}/apidocs/")
    app.run()
