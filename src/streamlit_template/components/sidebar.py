"""
Composant Sidebar avec logo pour l'application Streamlit
"""

import streamlit as st


def render_logo_placeholder():
    """
    Affiche un placeholder pour le logo dans la sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="
        text-align: center;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        <div style="
            font-size: 3rem;
            color: #666;
            margin-bottom: 0.5rem;
        ">🚀</div>
        <div style="
            font-size: 0.8rem;
            color: #666;
            font-style: italic;
        ">Logo Placeholder</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_info(app_version: str = "MVP 0.1.0"):
    """
    Affiche des informations sur l'application dans la sidebar
    
    Args:
        app_version: Version de l'application
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Informations")
    st.sidebar.info(f"""
    **Version:** {app_version}
    
    **Status:** Fonctionnel
    
    **Type:** Template Streamlit
    """)


def render_sidebar_navigation():
    """
    Affiche un menu de navigation dans la sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    st.sidebar.markdown("""
    - 🏠 **Home** - Page d'accueil
    - 📊 **Analytics** - Données et graphiques  
    - ⚙️ **Settings** - Configuration
    """)


def render_complete_sidebar():
    """
    Affiche une sidebar complète avec logo, navigation et informations
    """
    render_logo_placeholder()
    render_sidebar_navigation()
    render_sidebar_info()