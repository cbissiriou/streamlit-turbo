"""
Alembic environment configuration
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parents[4] / "src"))

# Import des modèles pour auto-génération
from streamlit_template.database.engine import get_database_url
from streamlit_template.database.models import SQLModel

# Configuration Alembic
config = context.config

# Interpréter le fichier de config pour le logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Métadonnées pour auto-migration
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """
    Migrations en mode 'offline' (génère juste le SQL)
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Migrations en mode 'online' (exécute sur la vraie DB)
    """
    # Récupérer l'URL depuis secrets.toml
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
