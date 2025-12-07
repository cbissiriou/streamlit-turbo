"""
Gestion des sessions et authentification utilisateur
"""

from datetime import datetime
from typing import Any

import streamlit as st
from sqlmodel import select

from streamlit_template.database import User as UserModel
from streamlit_template.database import get_session


def is_authenticated() -> bool:
    """
    Vérifie si l'utilisateur est authentifié

    Returns:
        bool: True si l'utilisateur est connecté
    """
    try:
        return st.user.is_logged_in
    except AttributeError:
        # Si st.user n'est pas disponible (auth non configurée)
        return False


def get_current_user() -> dict[str, Any] | None:
    """
    Récupère les informations de l'utilisateur connecté

    Returns:
        Dict avec les infos utilisateur ou None si non connecté
    """
    if not is_authenticated():
        return None

    try:
        return {
            "email": st.user.get("email"),
            "name": st.user.get("name"),
            "picture": st.user.get("picture"),
            "sub": st.user.get("sub"),  # Unique user ID
            "email_verified": st.user.get("email_verified", False),
        }
    except Exception:
        return None


def check_token_expiration() -> bool:
    """
    Vérifie si le token utilisateur a expiré

    Returns:
        bool: True si le token est encore valide
    """
    if not is_authenticated():
        return False

    try:
        exp = st.user.get("exp")
        if exp:
            expiration_time = datetime.fromtimestamp(exp)
            return datetime.now() < expiration_time
        return True  # Si pas d'expiration définie, considérer comme valide
    except Exception:
        return False


def logout_user():
    """Déconnecte l'utilisateur actuel"""
    try:
        st.logout()
    except Exception as e:
        st.error(f"Erreur lors de la déconnexion: {e}")


def check_auth() -> bool:
    """
    Vérifie l'authentification et redirige vers login si nécessaire

    Returns:
        bool: True si authentifié, False sinon
    """
    if not is_authenticated():
        return False

    # Vérifier l'expiration du token
    if not check_token_expiration():
        st.warning("Votre session a expiré. Veuillez vous reconnecter.")
        logout_user()
        return False

    return True


def get_user_role() -> str:
    """
    Récupère le rôle de l'utilisateur (à adapter selon votre logique)

    Returns:
        str: Rôle de l'utilisateur ('admin', 'user', etc.)
    """
    user = get_current_user()
    if not user:
        return "anonymous"

    # TODO: Implémenter la logique de rôles depuis la base de données
    # Pour l'instant, tous les utilisateurs authentifiés sont des "user"
    # Les admins pourraient être définis dans secrets.toml ou en base
    try:
        with next(get_session()) as session:
            statement = select(UserModel).where(UserModel.email == user["email"])
            db_user = session.exec(statement).first()
            if db_user:
                return db_user.role
            else:
                # Utilisateur pas encore en base, créer avec role "user"
                new_user = UserModel(
                    email=user["email"],
                    google_sub=user["sub"],
                    name=user.get("name"),
                    picture_url=user.get("picture"),
                    role="user",
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return "user"
    except Exception as e:
        admin_emails = st.secrets.get("admin_emails", [])
        if user.get("email") in admin_emails:
            return "admin"
        st.error(f"Erreur lors de la récupération du rôle: {e}")
        return "user"

    # admin_emails = st.secrets.get("admin_emails", [])
    # if user.get("email") in admin_emails:
    #     return "admin"

    # return "user"


def init_session_state():
    """Initialise les variables de session nécessaires"""
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()

    # Mettre à jour la dernière activité
    st.session_state.last_activity = datetime.now()
