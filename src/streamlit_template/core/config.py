"""
Configuration centralisée de l'application
"""

import os
from dataclasses import dataclass
from typing import Optional
import streamlit as st


@dataclass
class AppConfig:
    """Configuration de l'application"""
    
    # Informations de base
    app_name: str = "Streamlit Template"
    app_version: str = "MVP 0.1.0"
    app_description: str = "Template Streamlit avec architecture modulaire"
    
    # Configuration Streamlit
    page_title: str = "Streamlit Template"
    page_icon: str = "🚀"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    theme_mode: str = "auto"
    
    # Chemins
    data_dir: str = "data"
    assets_dir: str = "assets"
    
    # Base de données
    database_url: Optional[str] = None
    
    # Debug et logging
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # Cache
    cache_ttl: int = 3600  # 1 heure
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Crée la configuration depuis les variables d'environnement"""
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_version=os.getenv("APP_VERSION", cls.app_version),
            database_url=os.getenv("DATABASE_URL"),
            debug_mode=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            theme_mode=os.getenv("THEME_MODE", cls.theme_mode)
        )


def get_config() -> AppConfig:
    """Retourne la configuration de l'application"""
    if "app_config" not in st.session_state:
        st.session_state.app_config = AppConfig.from_env()
    return st.session_state.app_config


def update_config(**kwargs):
    """Met à jour la configuration"""
    config = get_config()
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    st.session_state.app_config = config