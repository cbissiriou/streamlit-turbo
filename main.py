#!/usr/bin/env python3
"""
StreamlitTurbo PRO - Production-ready Streamlit template
Version 1.0.0

Features:
- Google OAuth authentication
- SQLModel database (SQLite/PostgreSQL)
- Structured logging & analytics
- Modern navigation with st.navigation()
"""

import sys
from pathlib import Path

# Ajouter src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
from streamlit_template.database.engine import init_db
from streamlit_template.monitoring.logger import get_logger

# Configuration de la page
st.set_page_config(
    page_title="StreamlitTurbo PRO",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="collapsed",  # Pas de sidebar, navigation en haut
)

# Logger
logger = get_logger("main")

# Initialiser la base de données au démarrage
try:
    init_db()
    logger.info("database_initialized")
except Exception as e:
    logger.error("database_init_failed", error=str(e))


# Définition des pages avec navigation moderne
pages = [
    st.Page(
        "src/streamlit_template/pages/home.py",
        title="Accueil",
        icon=":material/home:",
        default=True,
    ),
    st.Page(
        "src/streamlit_template/pages/analytics.py",
        title="Analytics",
        icon=":material/insert_chart:",
    ),
    st.Page(
        "src/streamlit_template/pages/settings.py",
        title="Paramètres",
        icon=":material/settings:",
    ),
    st.Page(
        "src/streamlit_template/pages/admin.py",
        title="Admin",
        icon=":material/admin_panel_settings:",
    ),
]

# Navigation en position top (moderne)
page = st.navigation(pages, position="top")

# Exécution de la page sélectionnée
page.run()