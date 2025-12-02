"""
Tests unitaires pour le module d'authentification
"""

import pytest
from unittest.mock import Mock, patch, PropertyMock
from streamlit_template.auth.session import (
    is_authenticated,
    get_current_user,
    get_user_role,
)


class TestAuthSession:
    """Tests pour les fonctions de session"""

    def test_is_authenticated_when_logged_in(self):
        """Test: is_authenticated retourne True si user est connecté"""
        with patch("streamlit.user") as mock_user:
            mock_user.is_logged_in = True
            assert is_authenticated() is True

    def test_is_authenticated_when_logged_out(self):
        """Test: is_authenticated retourne False si user n'est pas connecté"""
        with patch("streamlit.user") as mock_user:
            mock_user.is_logged_in = False
            assert is_authenticated() is False

    def test_get_current_user_when_authenticated(self, sample_user_data):
        """Test: get_current_user retourne les données user si authentifié"""
        with patch("streamlit_template.auth.session.st") as mock_st:
            # Créer un mock user avec is_logged_in et get()
            mock_user = Mock()
            mock_user.is_logged_in = True
            mock_user.get = Mock(side_effect=lambda key, default=None: sample_user_data.get(key, default))
            mock_st.user = mock_user

            user = get_current_user()

            assert user is not None
            assert user["email"] == sample_user_data["email"]
            assert user["name"] == sample_user_data["name"]
            assert user["sub"] == sample_user_data["sub"]

    def test_get_current_user_when_not_authenticated(self):
        """Test: get_current_user retourne None si non authentifié"""
        with patch("streamlit.user") as mock_user:
            mock_user.is_logged_in = False

            user = get_current_user()

            assert user is None

    def test_get_user_role_admin(self, mock_streamlit_secrets):
        """Test: get_user_role retourne 'admin' pour un admin"""
        with patch("streamlit.user") as mock_user:
            mock_user.is_logged_in = True
            mock_user.get.return_value = "admin@example.com"

            with patch("streamlit_template.auth.session.get_current_user") as mock_get_user:
                mock_get_user.return_value = {"email": "admin@example.com"}

                role = get_user_role()

                assert role == "admin"

    def test_get_user_role_user(self, mock_streamlit_secrets):
        """Test: get_user_role retourne 'user' pour un utilisateur normal"""
        with patch("streamlit.user") as mock_user:
            mock_user.is_logged_in = True

            with patch("streamlit_template.auth.session.get_current_user") as mock_get_user:
                mock_get_user.return_value = {"email": "user@example.com"}

                role = get_user_role()

                assert role == "user"

    def test_get_user_role_anonymous(self):
        """Test: get_user_role retourne 'anonymous' si non connecté"""
        with patch("streamlit_template.auth.session.get_current_user") as mock_get_user:
            mock_get_user.return_value = None

            role = get_user_role()

            assert role == "anonymous"
