"""
Décorateurs pour la gestion de l'authentification et des autorisations
"""

import streamlit as st
from functools import wraps
from typing import Callable, List, Optional
from streamlit_template.auth.session import is_authenticated, get_user_role


def require_auth(func: Optional[Callable] = None, *, redirect_message: str = None):
    """
    Décorateur pour protéger une page/fonction nécessitant une authentification

    Usage:
        @require_auth
        def my_protected_page():
            st.write("Contenu protégé")

    Args:
        redirect_message: Message personnalisé affiché si non authentifié
    """
    if redirect_message is None:
        redirect_message = "Vous devez être connecté pour accéder à cette page."

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                st.warning(redirect_message)
                st.info("👇 Cliquez sur le bouton ci-dessous pour vous connecter")

                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🔐 Se connecter avec Google", use_container_width=True):
                        st.login()

                st.stop()

            return f(*args, **kwargs)

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def require_role(
    allowed_roles: List[str],
    denied_message: str = "Vous n'avez pas les permissions nécessaires."
):
    """
    Décorateur pour restreindre l'accès selon le rôle utilisateur

    Usage:
        @require_role(['admin'])
        def admin_page():
            st.write("Page admin")

    Args:
        allowed_roles: Liste des rôles autorisés
        denied_message: Message affiché si l'utilisateur n'a pas le bon rôle
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                st.warning("Vous devez être connecté pour accéder à cette page.")
                if st.button("🔐 Se connecter"):
                    st.login()
                st.stop()

            user_role = get_user_role()
            if user_role not in allowed_roles:
                st.error(denied_message)
                st.info(f"Votre rôle actuel: **{user_role}**")
                st.info(f"Rôles requis: **{', '.join(allowed_roles)}**")
                st.stop()

            return func(*args, **kwargs)

        return wrapper

    return decorator


def public_page(func: Callable) -> Callable:
    """
    Décorateur pour marquer une page comme publique (accessible sans auth)
    Utile pour la documentation et la clarté du code

    Usage:
        @public_page
        def home_page():
            st.write("Page publique")
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper._is_public = True
    return wrapper
