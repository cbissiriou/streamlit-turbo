"""
Configuration et gestion du moteur de base de données
"""

from collections.abc import Generator
from pathlib import Path

import streamlit as st
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine


def get_database_url() -> str:
    """
    Récupère l'URL de connexion à la base de données depuis secrets.toml

    Returns:
        str: URL de connexion (SQLite ou PostgreSQL)
    """
    # Essayer PostgreSQL en production
    if "database" in st.secrets and "postgresql" in st.secrets["database"]:
        pg_config = st.secrets["database"]["postgresql"]

        # Si URL complète fournie
        if "url" in pg_config:
            return pg_config["url"]

        # Sinon construire l'URL
        host = pg_config.get("host", "localhost")
        port = pg_config.get("port", 5432)
        database = pg_config.get("database", "streamlit_pro")
        username = pg_config.get("username", "postgres")
        password = pg_config.get("password", "")

        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

    # Sinon utiliser SQLite par défaut
    if "database" in st.secrets and "sqlite" in st.secrets["database"]:
        return st.secrets["database"]["sqlite"]["url"]

    # Fallback SQLite par défaut
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return f"sqlite:///{data_dir}/app.db"


_engine: Engine | None = None


def get_engine() -> Engine:
    """
    Retourne l'instance du moteur de base de données (singleton)

    Returns:
        Engine: Moteur SQLModel
    """
    global _engine

    if _engine is None:
        database_url = get_database_url()

        # Configuration selon le type de base
        connect_args = {}
        if database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        _engine = create_engine(
            database_url,
            echo=False,  # Mettre à True pour debug SQL
            connect_args=connect_args,
        )

    return _engine


def get_session() -> Generator[Session, None, None]:
    """
    Générateur de sessions de base de données

    Yields:
        Session: Session SQLModel
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialise la base de données (crée les tables)
    À appeler au démarrage de l'application
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def reset_db():
    """
    Réinitialise complètement la base de données
    ⚠️ ATTENTION: Supprime toutes les données !
    """
    engine = get_engine()
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
