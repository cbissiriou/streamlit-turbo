"""
Configuration et utilitaires de logging pour l'application
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st


class StreamlitLogHandler(logging.Handler):
    """Handler personnalisé pour afficher les logs dans Streamlit"""

    def __init__(self, container=None):
        super().__init__()
        self.container = container or st.container()
        self.log_messages = []

    def emit(self, record):
        """Émet un message de log"""
        msg = self.format(record)
        self.log_messages.append({
            'level': record.levelname,
            'message': msg,
            'timestamp': datetime.fromtimestamp(record.created)
        })

        # Limite le nombre de messages stockés
        if len(self.log_messages) > 100:
            self.log_messages = self.log_messages[-50:]

    def display_logs(self, max_messages: int = 20):
        """Affiche les logs dans Streamlit"""
        recent_logs = self.log_messages[-max_messages:]

        for log_entry in recent_logs:
            level = log_entry['level']
            message = log_entry['message']
            timestamp = log_entry['timestamp'].strftime("%H:%M:%S")

            if level == 'ERROR':
                st.error(f"[{timestamp}] {message}")
            elif level == 'WARNING':
                st.warning(f"[{timestamp}] {message}")
            elif level == 'INFO':
                st.info(f"[{timestamp}] {message}")
            else:
                st.text(f"[{timestamp}] {message}")


class ColoredFormatter(logging.Formatter):
    """Formateur avec couleurs pour la console"""

    # Codes couleur ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Vert
        'WARNING': '\033[33m',    # Jaune
        'ERROR': '\033[31m',      # Rouge
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        # Ajoute la couleur
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']

        # Format de base
        formatted = super().format(record)

        # Applique la couleur seulement au niveau
        parts = formatted.split(' - ', 2)
        if len(parts) >= 2:
            level_part = parts[0]
            message_part = ' - '.join(parts[1:])
            return f"{color}{level_part}{reset} - {message_part}"

        return f"{color}{formatted}{reset}"


def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
    enable_streamlit: bool = False,
    format_string: str | None = None
) -> logging.Logger:
    """
    Configure le système de logging
    
    Args:
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Chemin vers le fichier de log (optionnel)
        enable_streamlit: Active le handler Streamlit
        format_string: Format personnalisé des messages
    
    Returns:
        Logger configuré
    """

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Logger principal
    logger = logging.getLogger('streamlit_template')
    logger.setLevel(getattr(logging, level.upper()))

    # Évite la duplication des handlers
    if logger.handlers:
        logger.handlers.clear()

    # Handler console avec couleurs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    if sys.stdout.isatty():  # Terminal supportant les couleurs
        console_formatter = ColoredFormatter(format_string)
    else:
        console_formatter = logging.Formatter(format_string)

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Handler fichier si spécifié
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Handler Streamlit si demandé
    if enable_streamlit:
        streamlit_handler = StreamlitLogHandler()
        streamlit_handler.setLevel(logging.WARNING)  # Seulement les warnings et erreurs
        streamlit_formatter = logging.Formatter("%(levelname)s - %(message)s")
        streamlit_handler.setFormatter(streamlit_formatter)
        logger.addHandler(streamlit_handler)

        # Stocke le handler pour accès ultérieur
        if 'streamlit_log_handler' not in st.session_state:
            st.session_state.streamlit_log_handler = streamlit_handler

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Récupère un logger configuré
    
    Args:
        name: Nom du logger (optionnel)
    
    Returns:
        Instance du logger
    """
    if name is None:
        name = 'streamlit_template'

    logger = logging.getLogger(name)

    # Configure automatiquement si pas encore fait
    if not logger.handlers:
        return setup_logging()

    return logger


def log_function_execution(func_name: str, execution_time: float, **kwargs):
    """Log l'exécution d'une fonction avec ses métriques"""
    logger = get_logger()

    extra_info = ""
    if kwargs:
        extra_info = " - " + ", ".join([f"{k}={v}" for k, v in kwargs.items()])

    logger.info(f"Function {func_name} executed in {execution_time:.2f}s{extra_info}")


def log_user_action(action: str, user_id: str = None, **details):
    """Log une action utilisateur"""
    logger = get_logger()

    user_info = f"User {user_id}" if user_id else "Anonymous user"
    detail_str = ", ".join([f"{k}={v}" for k, v in details.items()]) if details else ""

    logger.info(f"{user_info} performed action: {action} - {detail_str}")


def log_data_operation(operation: str, dataset_name: str, record_count: int = None):
    """Log une opération sur les données"""
    logger = get_logger()

    count_info = f" ({record_count} records)" if record_count else ""
    logger.info(f"Data operation: {operation} on {dataset_name}{count_info}")


def display_log_viewer():
    """Affiche un visualiseur de logs dans Streamlit"""
    if 'streamlit_log_handler' in st.session_state:
        handler = st.session_state.streamlit_log_handler

        st.subheader("📋 Logs de l'application")

        if handler.log_messages:
            # Options de filtrage
            col1, col2 = st.columns([1, 1])

            with col1:
                level_filter = st.selectbox(
                    "Niveau minimum",
                    options=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    index=1
                )

            with col2:
                max_messages = st.number_input(
                    "Nombre max de messages",
                    min_value=10,
                    max_value=100,
                    value=20
                )

            # Filtre les messages
            level_hierarchy = {
                'DEBUG': 0, 'INFO': 1, 'WARNING': 2,
                'ERROR': 3, 'CRITICAL': 4
            }

            min_level = level_hierarchy[level_filter]
            filtered_logs = [
                log for log in handler.log_messages[-max_messages:]
                if level_hierarchy.get(log['level'], 0) >= min_level
            ]

            if filtered_logs:
                handler.display_logs(len(filtered_logs))
            else:
                st.info("Aucun log à afficher avec ces filtres.")
        else:
            st.info("Aucun log disponible pour le moment.")
    else:
        st.warning("Le visualiseur de logs n'est pas activé.")


def clear_logs():
    """Efface tous les logs stockés"""
    if 'streamlit_log_handler' in st.session_state:
        st.session_state.streamlit_log_handler.log_messages.clear()
        st.success("Logs effacés!")


# Configuration par défaut
DEFAULT_LOGGER = None


def init_default_logger(level: str = "INFO"):
    """Initialise le logger par défaut de l'application"""
    global DEFAULT_LOGGER
    if DEFAULT_LOGGER is None:
        DEFAULT_LOGGER = setup_logging(
            level=level,
            log_file="logs/app.log",
            enable_streamlit=True
        )
    return DEFAULT_LOGGER
