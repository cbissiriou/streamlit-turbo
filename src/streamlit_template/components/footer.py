"""
Composant Footer pour l'application Streamlit
"""

import streamlit as st
from datetime import datetime


def render_footer():
    """
    Affiche un footer standardisé pour l'application
    """
    st.markdown("---")
    st.markdown("""
    <div style="
        padding: 1rem 0;
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        border-top: 1px solid #f0f2f6;
        margin-top: 2rem;
    ">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("🚀 **Streamlit Template**")
    
    with col2:
        current_year = datetime.now().year
        st.markdown(f"© {current_year} - Développé avec Streamlit")
    
    with col3:
        st.markdown("Version MVP 0.1.0")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_footer_minimal():
    """
    Version minimaliste du footer
    """
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.7rem; padding: 1rem;">
        Streamlit Template MVP • © {year}
    </div>
    """.format(year=datetime.now().year), unsafe_allow_html=True)