"""
Module de monitoring et analytics
Logging structuré + tracking utilisateur simple
"""

from streamlit_template.monitoring.analytics import (
    get_app_stats,
    get_user_stats,
    track_action,
    track_page_view,
)
from streamlit_template.monitoring.logger import get_logger, log_event

__all__ = [
    "get_logger",
    "log_event",
    "track_page_view",
    "track_action",
    "get_user_stats",
    "get_app_stats",
]
