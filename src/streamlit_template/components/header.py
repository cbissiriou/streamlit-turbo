"""
Composant Header pour l'application Streamlit
"""

import streamlit as st


def render_header(title: str = "Streamlit Template", subtitle: str = None):
    """
    Affiche un header standardisé pour l'application
    
    Args:
        title: Titre principal à afficher
        subtitle: Sous-titre optionnel
    """
    st.markdown("""
    <div style="
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    ">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"🚀 {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")

    with col2:
        st.markdown("""
        <div style="text-align: right; padding-top: 1rem;">
            <small>Streamlit Template</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_navigation_breadcrumb(current_page: str):
    """
    Affiche un breadcrumb de navigation
    
    Args:
        current_page: Page actuelle pour le breadcrumb
    """
    st.markdown(f"""
    <nav style="margin-bottom: 1rem;">
        <small>🏠 Home > {current_page}</small>
    </nav>
    """, unsafe_allow_html=True)
