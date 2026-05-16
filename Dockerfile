# Image de base officielle Python 3.11 en version slim
FROM python:3.11-slim

#répertoire de travail à l’intérieur du conteneur
WORKDIR /app

# Copie des fichiers de dépendances en premier (cache Docker)
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY entrypoint.sh ./

# Installe uv puis synchronise les dépendances depuis uv.lock
# --no-dev  : exclut pytest, ruff et les autres outils de développement
# --system  : installe dans le Python système (pas de venv dans le conteneur)
RUN pip install uv && \
    uv sync --no-dev --system && \
    chmod +x entrypoint.sh && \
    mkdir -p data

# Port imposé par la consigne
EXPOSE 5000

# entrypoint.sh initialise la base au premier démarrage, puis lance gunicorn
ENTRYPOINT ["./entrypoint.sh"]
