"""
Page Paramètres - StreamlitTurbo PRO
Configuration utilisateur et préférences
"""

import streamlit as st
from streamlit_template.auth import require_auth, get_current_user
from streamlit_template.monitoring import track_page_view, track_action
from streamlit_template.components import render_header, render_footer

# Track page view
track_page_view("settings")

# Header
render_header("⚙️ Paramètres", "Configuration et préférences")


@require_auth
def render_settings_content():
    """Contenu de la page settings (protégé)"""

    user = get_current_user()

    # Onglets
    tab1, tab2, tab3 = st.tabs(["👤 Profil", "🎨 Affichage", "ℹ️ À propos"])

    with tab1:
        render_profile_tab(user)

    with tab2:
        render_display_tab()

    with tab3:
        render_about_tab()


def render_profile_tab(user):
    """Onglet profil utilisateur"""
    st.markdown("### 👤 Informations du profil")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Photo de profil
        if user.get("picture"):
            st.image(user["picture"], width=150)
        else:
            st.info("Pas de photo de profil")

    with col2:
        # Informations
        st.markdown(f"**Nom:** {user['name']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown(f"**ID:** `{user['sub'][:20]}...`")
        verified_badge = "✅" if user.get("email_verified") else "❌"
        st.markdown(f"**Email vérifié:** {verified_badge}")

    st.markdown("---")

    # Préférences utilisateur
    st.markdown("### 🔧 Préférences")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Langue",
            ["Français", "English", "Español", "Deutsch"],
            index=0,
        )

        timezone = st.selectbox(
            "Fuseau horaire",
            ["Europe/Paris", "UTC", "America/New_York", "Asia/Tokyo"],
            index=0,
        )

    with col2:
        notifications = st.checkbox("Notifications par email", value=True)

        newsletter = st.checkbox("Newsletter mensuelle", value=False)

    st.markdown("---")

    # Actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Sauvegarder", use_container_width=True, type="primary"):
            st.success("Préférences sauvegardées !")
            track_action("save_preferences", page="settings")

    with col2:
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.info("Préférences réinitialisées")

    with col3:
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.logout()


def render_display_tab():
    """Onglet affichage"""
    st.markdown("### 🎨 Apparence")

    st.info(
        """
    **Configuration du thème:**

    Pour changer le thème de l'application, modifiez le fichier `.streamlit/config.toml` :

    - **Theme Blue (Corporate)** - Thème professionnel par défaut
    - **Theme Dark (Spotify)** - Thème sombre moderne
    - **Theme Light (Eclair)** - Thème clair élégant
    - **Theme Green (Nature)** - Thème nature moderne

    Décommentez le thème désiré dans le fichier de configuration.
    """
    )

    st.markdown("---")

    st.markdown("### 📐 Mise en page")

    layout_pref = st.radio(
        "Largeur de page",
        ["Large (wide)", "Centré (centered)"],
        index=0,
    )

    show_footer = st.checkbox("Afficher le footer", value=True)

    animations = st.checkbox("Activer les animations", value=True)

    st.markdown("---")

    if st.button("💾 Sauvegarder l'affichage", use_container_width=True, type="primary"):
        st.success("Préférences d'affichage sauvegardées !")
        track_action("save_display_prefs", page="settings")


def render_about_tab():
    """Onglet à propos"""
    st.markdown("### ℹ️ À propos de l'application")

    st.markdown("""
    **StreamlitTurbo PRO**
    Version 1.0.0

    Template professionnel pour applications Streamlit avec fonctionnalités enterprise.

    ---

    #### 🚀 Fonctionnalités

    - ✅ Authentification Google OAuth
    - ✅ Base de données SQLModel
    - ✅ Monitoring & Analytics
    - ✅ GitHub Actions CI/CD
    - ✅ Docker support
    - ✅ Tests automatisés

    ---

    #### 📚 Documentation

    - [README.md](/) - Guide complet
    - [CLAUDE.md](/) - Guide pour Claude Code
    - [GitHub](https://github.com/gpenessot/ultimate-streamlit-template) - Code source

    ---

    #### 👨‍💻 Auteur

    **Gaël Penessot**
    📧 gael.penessot@gmail.com
    💼 [LinkedIn](https://www.linkedin.com/in/gael-penessot/)

    ---

    #### 📄 Licence

    MIT License - Libre d'utilisation et de modification

    ---

    #### 🛠️ Technologies

    - Python 3.12+
    - Streamlit 1.40+
    - SQLModel
    - Alembic
    - Plotly
    - structlog
    """)

    st.markdown("---")

    # Statistiques système
    with st.expander("🔧 Informations système"):
        import sys
        import platform

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Python:** {sys.version.split()[0]}")
            st.markdown(f"**Streamlit:** {st.__version__}")
            st.markdown(f"**Plateforme:** {platform.system()}")

        with col2:
            st.markdown(f"**Architecture:** {platform.machine()}")
            st.markdown(f"**Processeur:** {platform.processor()}")


# Render le contenu avec protection auth
render_settings_content()

# Footer
render_footer()
