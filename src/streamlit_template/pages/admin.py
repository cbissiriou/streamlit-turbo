"""
Page Admin - StreamlitTurbo PRO
Administration et gestion (réservé aux admins)
"""

import streamlit as st

from streamlit_template.auth import get_current_user, require_role
from streamlit_template.components import render_footer, render_header
from streamlit_template.monitoring import get_app_stats, get_user_stats, track_page_view

# Track page view
track_page_view("admin")

# Header
render_header("🛡️ Administration", "Panneau d'administration (accès restreint)")


@require_role(["admin"], denied_message="Cette page est réservée aux administrateurs.")
def render_admin_content():
    """Contenu de la page admin (réservé aux admins)"""

    user = get_current_user()

    st.success(f"Bienvenue dans le panneau d'administration, **{user['name']}** !")

    # Onglets admin
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Statistiques", "👥 Utilisateurs", "🗄️ Base de données", "⚙️ Système"]
    )

    with tab1:
        render_stats_tab()

    with tab2:
        render_users_tab()

    with tab3:
        render_database_tab()

    with tab4:
        render_system_tab()


def render_stats_tab():
    """Onglet statistiques globales"""
    st.markdown("### 📊 Statistiques de l'application")

    # Récupérer les stats
    stats = get_app_stats()

    if "error" in stats:
        st.error(f"Erreur lors de la récupération des stats: {stats['error']}")
        st.info("Assurez-vous que la base de données est initialisée et accessible.")
        return

    # Métriques globales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Utilisateurs totaux",
            value=stats.get("total_users", 0),
        )

    with col2:
        st.metric(
            label="✅ Utilisateurs actifs",
            value=stats.get("active_users", 0),
        )

    with col3:
        st.metric(
            label="🎯 Actions totales",
            value=stats.get("total_actions", 0),
        )

    with col4:
        engagement_rate = (
            (stats.get("active_users", 0) / stats.get("total_users", 1) * 100)
            if stats.get("total_users", 0) > 0
            else 0
        )
        st.metric(
            label="📈 Taux engagement",
            value=f"{engagement_rate:.1f}%",
        )

    st.markdown("---")

    # Activité récente
    st.markdown("### 📋 Activité récente")
    st.info("Les logs d'activité détaillés seront affichés ici.")

    # Exemple de tableau d'activité
    from datetime import datetime, timedelta

    import pandas as pd

    activity_data = pd.DataFrame(
        {
            "Date": [datetime.now() - timedelta(hours=i) for i in range(10)],
            "Utilisateur": [f"user{i}@example.com" for i in range(10)],
            "Action": ["page_view", "button_click"] * 5,
            "Page": ["home", "analytics", "settings"] * 3 + ["admin"],
        }
    )

    st.dataframe(activity_data, use_container_width=True, hide_index=True)


def render_users_tab():
    """Onglet gestion utilisateurs"""
    st.markdown("### 👥 Gestion des utilisateurs")

    st.info(
        """
    **Fonctionnalités à venir:**
    - Liste de tous les utilisateurs
    - Modification des rôles
    - Suspension/activation de comptes
    - Statistiques par utilisateur
    """
    )

    # Recherche d'utilisateur
    search_email = st.text_input("🔍 Rechercher un utilisateur par email")

    if search_email:
        user_stats = get_user_stats(search_email)

        if "error" in user_stats:
            st.warning(f"Utilisateur non trouvé ou erreur: {user_stats['error']}")
        else:
            st.success(f"Utilisateur trouvé: {search_email}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Actions totales",
                    user_stats.get("total_actions", 0),
                )

            with col2:
                most_visited = user_stats.get("most_visited_pages", [])
                if most_visited:
                    top_page = most_visited[0]["page"]
                    st.metric("Page favorite", top_page or "N/A")

            # Détails
            if most_visited:
                st.markdown("**Pages les plus visitées:**")
                for item in most_visited:
                    st.write(f"- {item['page']}: {item['count']} visites")


def render_database_tab():
    """Onglet base de données"""
    st.markdown("### 🗄️ Gestion de la base de données")

    # Infos connexion
    st.markdown("#### Connexion")

    try:
        from streamlit_template.database.engine import get_database_url

        db_url = get_database_url()

        # Masquer le mot de passe
        safe_url = db_url.split("@")[-1] if "@" in db_url else db_url

        st.code(f"Database: {safe_url}")

        if db_url.startswith("sqlite"):
            st.info("🗄️ Base de données SQLite (développement)")
        else:
            st.success("🚀 Base de données PostgreSQL (production)")

    except Exception as e:
        st.error(f"Erreur de connexion: {e}")

    st.markdown("---")

    # Migrations
    st.markdown("#### Migrations")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Vérifier migrations", use_container_width=True):
            st.info("Utilisez `just db-history` dans le terminal")

    with col2:
        if st.button("⬆️ Appliquer migrations", use_container_width=True):
            st.warning("Utilisez `just db-upgrade` dans le terminal")

    with col3:
        if st.button("📋 Nouvelle migration", use_container_width=True):
            st.info("Utilisez `just db-migrate 'description'` dans le terminal")

    st.markdown("---")

    # Actions dangereuses
    with st.expander("⚠️ Actions dangereuses"):
        st.warning("**ATTENTION**: Ces actions sont irréversibles !")

        if st.button("🗑️ Réinitialiser la base de données"):
            st.error("Fonctionnalité désactivée pour votre sécurité. Utilisez le terminal.")


def render_system_tab():
    """Onglet système"""
    st.markdown("### ⚙️ Informations système")

    import platform
    import sys

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🐍 Python")
        st.code(f"Version: {sys.version.split()[0]}")
        st.code(f"Executable: {sys.executable}")

        st.markdown("#### 📊 Streamlit")
        st.code(f"Version: {st.__version__}")

    with col2:
        st.markdown("#### 💻 Système")
        st.code(f"OS: {platform.system()}")
        st.code(f"Architecture: {platform.machine()}")
        st.code(f"Processeur: {platform.processor()}")

    st.markdown("---")

    # Variables d'environnement (sans secrets)
    with st.expander("🔐 Configuration (secrets masqués)"):
        st.info("Les secrets sont chargés depuis `.streamlit/secrets.toml`")

        if "auth" in st.secrets:
            st.success("✅ Authentification configurée")
        else:
            st.warning("❌ Authentification non configurée")

        if "database" in st.secrets:
            st.success("✅ Base de données configurée")
        else:
            st.warning("❌ Base de données non configurée")

    st.markdown("---")

    # Logs
    st.markdown("### 📋 Logs système")

    log_level = st.selectbox("Niveau de log", ["INFO", "DEBUG", "WARNING", "ERROR"])

    st.info("Les logs structurés sont affichés dans le terminal avec `structlog`.")

    # Boutons d'action
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Redémarrer l'app", use_container_width=True):
            st.info("Utilisez `Ctrl+C` puis `just run` dans le terminal")

    with col2:
        if st.button("🧹 Nettoyer cache", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache nettoyé !")
            st.rerun()


# Render le contenu avec protection role
render_admin_content()

# Footer
render_footer()
