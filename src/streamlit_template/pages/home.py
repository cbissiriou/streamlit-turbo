"""
Page d'accueil - StreamlitTurbo PRO
"""

import streamlit as st

from streamlit_template.auth import get_current_user, is_authenticated
from streamlit_template.components import render_footer, render_header
from streamlit_template.monitoring import track_page_view

# Track page view
track_page_view("home")

# Header
render_header("🚀 StreamlitTurbo PRO", "Production-ready Streamlit template")

# Section authentification
if not is_authenticated():
    # Page publique - Présentation du template
    st.markdown("""
    ## Bienvenue sur StreamlitTurbo PRO

    Template professionnel pour applications Streamlit avec fonctionnalités enterprise :

    ### ✨ Fonctionnalités Principales

    #### 🔐 Authentification
    - Google OAuth natif (via `st.login()`)
    - Gestion des sessions sécurisée
    - Système de rôles et permissions

    #### 🗄️ Base de Données
    - SQLModel (ORM moderne basé sur Pydantic)
    - Support SQLite (dev) et PostgreSQL (prod)
    - Migrations Alembic intégrées

    #### 📊 Monitoring & Analytics
    - Logging structuré (structlog)
    - Tracking des actions utilisateurs
    - Analytics intégrés

    #### 🚀 DevOps & Déploiement
    - GitHub Actions (CI/CD)
    - Docker + docker-compose
    - Pre-commit hooks
    - Tests automatisés (pytest)

    #### 🎨 Interface Moderne
    - Navigation top (sans sidebar)
    - 4 thèmes professionnels
    - Composants réutilisables
    - Design responsive

    ---

    ### 🎯 Démarrage Rapide

    ```bash
    # Setup
    just setup

    # Lancer l'app
    just run

    # Mode dev
    just dev
    ```

    ### 📚 Documentation

    - **README.md** - Guide complet
    - **CLAUDE.md** - Guide pour Claude Code
    - **justfile** - Toutes les commandes disponibles
    """)

    # Call to action
    st.markdown("---")
    st.subheader("🔑 Connexion")
    st.info("Connectez-vous pour accéder aux fonctionnalités complètes")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Se connecter avec Google", use_container_width=True, type="primary"):
            st.login()

else:
    # Page authentifiée - Dashboard personnalisé
    user = get_current_user()

    st.success(f"👋 Bonjour **{user['name']}** !")

    # KPIs en haut
    st.markdown("### 📊 Vue d'ensemble")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🎯 Status",
            value="Actif",
            delta="Connecté",
        )

    with col2:
        from streamlit_template.auth.session import get_user_role

        st.metric(
            label="👤 Rôle",
            value=get_user_role().title(),
        )

    with col3:
        email_display = user["email"][:20] + "..." if len(user["email"]) > 20 else user["email"]
        st.metric(
            label="📧 Email",
            value=email_display,
        )

    with col4:
        st.metric(
            label="✅ Vérifié",
            value="Oui" if user.get("email_verified") else "Non",
        )

    st.markdown("---")

    # Navigation rapide
    st.markdown("### 🧭 Navigation Rapide")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 📊 Analytics
        Visualisez vos données avec des graphiques interactifs et des KPIs en temps réel.

        Utilisez le menu de navigation en haut pour accéder.
        """)

    with col2:
        st.markdown("""
        #### ⚙️ Paramètres
        Configurez votre profil, vos préférences et l'application.

        Utilisez le menu de navigation en haut pour accéder.
        """)

    with col3:
        st.markdown("""
        #### 🛡️ Admin
        Gestion des utilisateurs et statistiques de l'application (réservé aux admins).

        Utilisez le menu de navigation en haut pour accéder.
        """)

    st.markdown("---")

    # Informations utilisateur
    with st.expander("ℹ️ Informations détaillées"):
        st.json({
            "email": user["email"],
            "name": user["name"],
            "sub": user["sub"],
            "email_verified": user.get("email_verified", False),
            "picture": user.get("picture", "N/A"),
        })

    # Quick actions
    st.markdown("### ⚡ Actions Rapides")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 Nouvelle entrée", use_container_width=True):
            st.info("Fonctionnalité à implémenter")

    with col2:
        if st.button("📈 Rapport", use_container_width=True):
            st.info("Fonctionnalité à implémenter")

    with col3:
        if st.button("💾 Exporter données", use_container_width=True):
            st.info("Fonctionnalité à implémenter")

    with col4:
        if st.button("🔔 Notifications", use_container_width=True):
            st.info("Aucune notification")

# Footer
render_footer()
