# StreamlitTurbo PRO - Justfile
# Compatible Windows, Linux, macOS

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Variables
PYTHON_VERSION := "3.12"
PROJECT_NAME := "streamlit-template-pro"

# Setup complet du projet
setup:
    @echo "Configuration du projet StreamlitTurbo PRO..."
    uv venv --python {{PYTHON_VERSION}}
    @echo "Synchronisation des dependances avec le venv..."
    uv sync --python .venv/bin/python
    @echo "Installation des pre-commit hooks..."
    uv run --python {{PYTHON_VERSION}} pre-commit install
    @echo "Setup termine! Utilisez 'just run' pour lancer l'application."

# Lancement de l'application
run:
    uv run --python 3.12 streamlit run main.py

# Synchronisation des dependances
sync:
    uv sync --python .venv/bin/python

# Ajout d'une dependance
add PACKAGE:
    uv add {{PACKAGE}}

# Ajout d'une dependance de dev
add-dev PACKAGE:
    uv add --group dev {{PACKAGE}}

# Formatage du code avec ruff
format:
    @echo "Formatage du code avec ruff..."
    uv run ruff format .
    @echo "Done!"

# Verification de la qualite du code avec ruff
lint:
    @echo "Verification du code avec ruff..."
    uv run ruff check .
    @echo "All checks passed!"

# Formatage ET verification (combo pratique)
check: format lint

# Type checking avec mypy
typecheck:
    @echo "Verification des types avec mypy..."
    uv run mypy src/
    @echo "Type checking complete!"

# Generation du requirements.txt
requirements:
    uv pip compile pyproject.toml -o requirements.txt

# Creation de l'environnement virtuel
venv:
    uv venv --python {{PYTHON_VERSION}}

# Nettoyage (compatible toutes plateformes via Python)
clean:
    python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('.venv'), pathlib.Path('__pycache__'), pathlib.Path('.pytest_cache'), pathlib.Path('.ruff_cache'), pathlib.Path('htmlcov')] if p.exists()]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"

# Reinstallation complete
reset: clean setup

# Mode developpement avec auto-reload
dev:
    uv run --python 3.12 streamlit run main.py --server.runOnSave=true --global.developmentMode=true

# Lancer tous les tests
test:
    uv run pytest tests/ -v

# Tests avec coverage
test-cov:
    uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Tests unitaires uniquement
test-unit:
    uv run pytest tests/unit/ -v

# Tests d'integration uniquement
test-integration:
    uv run pytest tests/integration/ -v

# Lancer pre-commit sur tous les fichiers
pre-commit:
    uv run pre-commit run --all-files

# Migrations base de donnees - Creer une nouvelle migration
db-migrate MESSAGE:
    uv run alembic revision --autogenerate -m "{{MESSAGE}}"

# Migrations - Appliquer les migrations
db-upgrade:
    uv run alembic upgrade head

# Migrations - Revenir en arriere
db-downgrade:
    uv run alembic downgrade -1

# Migrations - Voir l'historique
db-history:
    uv run alembic history

# Docker - Build l'image
docker-build:
    docker build -t {{PROJECT_NAME}}:latest -f docker/Dockerfile .

# Docker - Lancer avec docker-compose
docker-up:
    docker-compose -f docker/docker-compose.yml up -d

# Docker - Arreter les conteneurs
docker-down:
    docker-compose -f docker/docker-compose.yml down

# Docker - Voir les logs
docker-logs:
    docker-compose -f docker/docker-compose.yml logs -f

# Informations sur le projet
info:
    @echo "StreamlitTurbo PRO"
    @echo "  Version: 1.0.0"
    @echo "  Python: {{PYTHON_VERSION}}"
    @echo "  Auteur: Gael Penessot"

# Aide - Afficher toutes les commandes
help:
    @echo "StreamlitTurbo PRO - Commandes disponibles"
    @echo ""
    @echo "🚀 Principales:"
    @echo "  just setup              - Setup complet du projet"
    @echo "  just run                - Lancer l'application"
    @echo "  just dev                - Mode developpement (auto-reload)"
    @echo ""
    @echo "🔍 Qualite du code:"
    @echo "  just format             - Formater le code"
    @echo "  just lint               - Verifier la qualite"
    @echo "  just check              - Format + Lint"
    @echo "  just typecheck          - Verification des types"
    @echo "  just pre-commit         - Lancer pre-commit sur tous les fichiers"
    @echo ""
    @echo "📦 Dependances:"
    @echo "  just sync               - Synchroniser"
    @echo "  just add PACKAGE        - Ajouter une lib"
    @echo "  just add-dev PACKAGE    - Ajouter une lib de dev"
    @echo "  just requirements       - Generer requirements.txt"
    @echo ""
    @echo "✅ Tests:"
    @echo "  just test               - Lancer tous les tests"
    @echo "  just test-cov           - Tests avec coverage"
    @echo "  just test-unit          - Tests unitaires uniquement"
    @echo "  just test-integration   - Tests d'integration uniquement"
    @echo ""
    @echo "🗄️  Base de donnees:"
    @echo "  just db-migrate MSG     - Creer une migration"
    @echo "  just db-upgrade         - Appliquer les migrations"
    @echo "  just db-downgrade       - Revenir en arriere"
    @echo "  just db-history         - Voir l'historique"
    @echo ""
    @echo "🐳 Docker:"
    @echo "  just docker-build       - Build l'image Docker"
    @echo "  just docker-up          - Lancer avec docker-compose"
    @echo "  just docker-down        - Arreter les conteneurs"
    @echo "  just docker-logs        - Voir les logs"
    @echo ""
    @echo "🛠️  Maintenance:"
    @echo "  just clean              - Nettoyer"
    @echo "  just reset              - Reinstaller"
    @echo "  just info               - Informations projet"

# Commande par defaut
default: help
