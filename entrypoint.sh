#!/bin/sh
set -e

# Lance db_init uniquement si la base n'existe pas encore (premier démarrage).
# pour éviter que reset_database() n'efface les données à chaque redémarrage.
if [ ! -f /app/data/parashop.db ]; then
    echo "Première exécution : initialisation de la base de données..."
    python -m src.db_init
    echo "Base initialisée avec succès."
else
    echo "Base de données existante détectée, initialisation ignorée."
fi

# Remplace le processus shell par gunicorn (bonne gestion des signaux Docker)
exec gunicorn --bind 0.0.0.0:5000 --workers 2 src.app:app
