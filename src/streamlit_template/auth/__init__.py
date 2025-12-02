"""
Module d'authentification pour StreamlitTurbo PRO
Utilise l'authentification native Streamlit avec Google OAuth
"""

from streamlit_template.auth.decorators import require_auth, require_role
from streamlit_template.auth.session import (
    check_auth,
    get_current_user,
    is_authenticated,
    logout_user,
)

__all__ = [
    "require_auth",
    "require_role",
    "check_auth",
    "get_current_user",
    "is_authenticated",
    "logout_user",
]
