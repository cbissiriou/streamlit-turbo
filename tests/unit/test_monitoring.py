"""
Tests unitaires pour le module monitoring
"""

import pytest
from unittest.mock import patch, Mock
from streamlit_template.monitoring.logger import get_logger, log_event
from streamlit_template.monitoring.analytics import track_page_view, track_action


class TestLogger:
    """Tests pour le système de logging"""

    def test_get_logger_returns_logger(self):
        """Test: get_logger retourne un logger"""
        logger = get_logger("test")

        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "warning")

    def test_log_event_with_context(self):
        """Test: log_event avec contexte"""
        with patch("streamlit_template.monitoring.logger.get_logger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            log_event("test_event", user="test@example.com", action="click")

            mock_logger.info.assert_called_once_with(
                "test_event", user="test@example.com", action="click"
            )


class TestAnalytics:
    """Tests pour le système d'analytics"""

    def test_track_page_view_when_analytics_disabled(self, mock_streamlit_secrets):
        """Test: track_page_view ne sauvegarde pas si analytics désactivé"""
        mock_streamlit_secrets._data["monitoring"]["enable_analytics"] = False

        with patch("streamlit_template.monitoring.analytics.get_session") as mock_session:
            track_page_view("home")

            # Ne devrait pas avoir appelé la session DB
            mock_session.assert_not_called()

    def test_track_page_view_when_analytics_enabled(self, mock_streamlit_secrets):
        """Test: track_page_view sauvegarde si analytics activé"""
        mock_streamlit_secrets._data["monitoring"]["enable_analytics"] = True

        with patch("streamlit_template.monitoring.analytics.get_session") as mock_get_session:
            with patch("streamlit_template.monitoring.analytics.get_current_user") as mock_user:
                mock_user.return_value = {"email": "test@example.com"}

                # Créer un mock de session DB qui supporte le context manager
                mock_db_session = Mock()
                mock_db_session.__enter__ = Mock(return_value=mock_db_session)
                mock_db_session.__exit__ = Mock(return_value=False)

                # get_session() retourne un générateur, donc on utilise iter() pour next()
                mock_get_session.return_value = iter([mock_db_session])

                track_page_view("analytics")

                # Devrait avoir sauvegardé en DB
                mock_db_session.add.assert_called_once()
                mock_db_session.commit.assert_called_once()

    def test_track_action_with_details(self, mock_streamlit_secrets):
        """Test: track_action avec détails"""
        mock_streamlit_secrets._data["monitoring"]["enable_analytics"] = True

        with patch("streamlit_template.monitoring.analytics.get_session") as mock_get_session:
            with patch("streamlit_template.monitoring.analytics.get_current_user") as mock_user:
                mock_user.return_value = {"email": "test@example.com"}

                # Créer un mock de session DB qui supporte le context manager
                mock_db_session = Mock()
                mock_db_session.__enter__ = Mock(return_value=mock_db_session)
                mock_db_session.__exit__ = Mock(return_value=False)

                # get_session() retourne un générateur, donc on utilise iter() pour next()
                mock_get_session.return_value = iter([mock_db_session])

                track_action("button_click", details={"button": "export"}, page="analytics")

                mock_db_session.add.assert_called_once()

                # Vérifier que les détails sont stockés
                call_args = mock_db_session.add.call_args[0][0]
                assert call_args.action == "button_click"
                assert call_args.page == "analytics"
                assert '"button": "export"' in call_args.details

    def test_track_action_handles_errors_gracefully(self, mock_streamlit_secrets):
        """Test: track_action gère les erreurs sans crasher"""
        mock_streamlit_secrets._data["monitoring"]["enable_analytics"] = True

        with patch("streamlit_template.monitoring.analytics.get_session") as mock_session:
            mock_session.side_effect = Exception("DB error")

            # Ne devrait pas lever d'exception
            track_action("test_action")
