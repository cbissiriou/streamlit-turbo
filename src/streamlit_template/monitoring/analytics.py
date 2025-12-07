"""
Analytics simples pour tracking utilisateur
"""

from datetime import datetime
from typing import Any

import streamlit as st

from streamlit_template.auth.session import get_current_user
from streamlit_template.database.engine import get_session
from streamlit_template.database.models import ActivityLog
from streamlit_template.monitoring.logger import log_event


def track_page_view(page_name: str):
    """
    Track une visite de page

    Args:
        page_name: Nom de la page visitée
    """
    user = get_current_user()
    user_email = user.get("email") if user else "anonymous"

    # Log pour debug
    log_event(
        "page_view",
        page=page_name,
        user=user_email,
    )

    # Stocker en base si analytics activé
    if st.secrets.get("monitoring", {}).get("enable_analytics", False):
        try:
            with next(get_session()) as session:
                log_entry = ActivityLog(
                    user_email=user_email,
                    action="page_view",
                    page=page_name,
                    timestamp=datetime.now(),
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            # Ne pas bloquer l'app si le logging échoue
            log_event("analytics_error", error=str(e))


def track_action(action: str, details: dict[str, Any] | None = None, page: str | None = None):
    """
    Track une action utilisateur

    Args:
        action: Type d'action (button_click, form_submit, etc.)
        details: Détails additionnels (stockés en JSON)
        page: Page où l'action a eu lieu
    """
    user = get_current_user()
    user_email = user.get("email") if user else "anonymous"

    import json

    details_json = json.dumps(details) if details else None

    log_event("user_action", action=action, user=user_email, page=page, details=details)

    if st.secrets.get("monitoring", {}).get("enable_analytics", False):
        try:
            with next(get_session()) as session:
                log_entry = ActivityLog(
                    user_email=user_email,
                    action=action,
                    page=page,
                    details=details_json,
                    timestamp=datetime.now(),
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            log_event("analytics_error", error=str(e))


def get_user_stats(user_email: str) -> dict[str, Any]:
    """
    Récupère les statistiques d'un utilisateur

    Args:
        user_email: Email de l'utilisateur

    Returns:
        Dict avec les stats
    """
    try:
        with next(get_session()) as session:
            from sqlmodel import func, select

            # Nombre total d'actions
            total_actions = session.exec(
                select(func.count(ActivityLog.id)).where(ActivityLog.user_email == user_email)
            ).one()

            # Pages les plus visitées
            most_visited = session.exec(
                select(ActivityLog.page, func.count(ActivityLog.id))
                .where(ActivityLog.user_email == user_email)
                .where(ActivityLog.action == "page_view")
                .group_by(ActivityLog.page)
                .order_by(func.count(ActivityLog.id).desc())
                .limit(5)
            ).all()

            return {
                "total_actions": total_actions,
                "most_visited_pages": [
                    {"page": page, "count": count} for page, count in most_visited
                ],
            }
    except Exception as e:
        log_event("stats_error", error=str(e))
        return {"error": str(e)}


def get_app_stats() -> dict[str, Any]:
    """
    Récupère les statistiques globales de l'application

    Returns:
        Dict avec les stats globales
    """
    try:
        with next(get_session()) as session:
            from sqlmodel import func, select

            from streamlit_template.database.models import User

            # Nombre d'utilisateurs
            total_users = session.exec(select(func.count(User.id))).one()

            # Nombre d'actions
            total_actions = session.exec(select(func.count(ActivityLog.id))).one()

            # Utilisateurs actifs (avec au moins une action)
            active_users = session.exec(
                select(func.count(func.distinct(ActivityLog.user_email)))
            ).one()

            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_actions": total_actions,
            }
    except Exception as e:
        log_event("app_stats_error", error=str(e))
        return {"error": str(e)}
