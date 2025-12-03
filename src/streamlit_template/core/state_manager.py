"""
Gestionnaire d'état global de l'application
"""

from dataclasses import dataclass, field
from typing import Any

import streamlit as st


@dataclass
class AppState:
    """État global de l'application"""

    # État utilisateur
    user_id: str | None = None
    user_name: str | None = None
    is_authenticated: bool = False

    # Navigation
    current_page: str = "Home"
    previous_page: str | None = None

    # Données
    data_cache: dict[str, Any] = field(default_factory=dict)

    # UI State
    sidebar_collapsed: bool = False
    theme: str = "auto"

    # Erreurs et notifications
    last_error: str | None = None
    notifications: list = field(default_factory=list)


def initialize_state():
    """Initialise l'état de l'application"""
    if "app_state" not in st.session_state:
        st.session_state.app_state = AppState()


def get_state() -> AppState:
    """Récupère l'état actuel de l'application"""
    initialize_state()
    return st.session_state.app_state


def update_state(**kwargs):
    """Met à jour l'état de l'application"""
    state = get_state()
    for key, value in kwargs.items():
        if hasattr(state, key):
            setattr(state, key, value)


def reset_state():
    """Remet l'état à zéro"""
    st.session_state.app_state = AppState()


def set_current_page(page_name: str):
    """Change la page courante"""
    state = get_state()
    state.previous_page = state.current_page
    state.current_page = page_name


def add_notification(message: str, type: str = "info"):
    """Ajoute une notification"""
    state = get_state()
    state.notifications.append({
        "message": message,
        "type": type,
        "timestamp": st.session_state.get("timestamp", 0)
    })


def clear_notifications():
    """Efface toutes les notifications"""
    state = get_state()
    state.notifications.clear()


def set_error(error_message: str):
    """Enregistre une erreur"""
    state = get_state()
    state.last_error = error_message
    add_notification(error_message, "error")


def clear_error():
    """Efface l'erreur courante"""
    state = get_state()
    state.last_error = None


def cache_data(key: str, data: Any):
    """Met en cache des données"""
    state = get_state()
    state.data_cache[key] = data


def get_cached_data(key: str, default: Any = None) -> Any:
    """Récupère des données du cache"""
    state = get_state()
    return state.data_cache.get(key, default)


def clear_cache(key: str | None = None):
    """Efface le cache"""
    state = get_state()
    if key:
        state.data_cache.pop(key, None)
    else:
        state.data_cache.clear()
