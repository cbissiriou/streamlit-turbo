"""
Module de monitoring et analytics
Logging structuré + tracking utilisateur simple
"""

from streamlit_template.monitoring.logger import get_logger, log_event
from streamlit_template.monitoring.analytics import track_page_view, track_action, get_user_stats, get_app_stats

__all__ = ["get_logger", "log_event", "track_page_view", "track_action", "get_user_stats", "get_app_stats"]
