"""
Système de logging structuré avec structlog
"""

import structlog
import logging
import sys
from pathlib import Path

# Configuration du logging structuré
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer() if sys.stderr.isatty() else structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)


def get_logger(name: str = "streamlit_app") -> structlog.BoundLogger:
    """
    Récupère un logger structuré

    Args:
        name: Nom du logger

    Returns:
        Logger structlog
    """
    return structlog.get_logger(name)


def log_event(event: str, **kwargs):
    """
    Log un événement avec contexte

    Args:
        event: Description de l'événement
        **kwargs: Contexte additionnel
    """
    logger = get_logger()
    logger.info(event, **kwargs)


def setup_file_logging(log_dir: str = "logs"):
    """
    Configure le logging dans des fichiers

    Args:
        log_dir: Répertoire pour les logs
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Handler pour fichier
    file_handler = logging.FileHandler(log_path / "app.log")
    file_handler.setLevel(logging.INFO)

    # Format JSON pour parsing facile
    file_handler.setFormatter(
        logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    )

    # Ajouter au logger root
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
