"""
Configuration pytest et fixtures communes
"""

import pytest
import sys
from pathlib import Path

# Ajouter src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_user_data():
    """Fixture: données utilisateur pour les tests"""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "sub": "123456789",
        "email_verified": True,
        "picture": "https://example.com/photo.jpg",
    }


@pytest.fixture
def sample_admin_data():
    """Fixture: données admin pour les tests"""
    return {
        "email": "admin@example.com",
        "name": "Admin User",
        "sub": "987654321",
        "email_verified": True,
    }


@pytest.fixture
def test_db_url():
    """Fixture: URL de base de données de test (SQLite en mémoire)"""
    return "sqlite:///:memory:"


@pytest.fixture
def mock_streamlit_secrets(monkeypatch):
    """Fixture: Mock des secrets Streamlit"""

    class MockSecrets:
        def __init__(self):
            self._data = {
                "auth": {
                    "redirect_uri": "http://localhost:8501/oauth2callback",
                    "cookie_secret": "test-secret-key-for-testing-only",
                    "client_id": "test-client-id",
                    "client_secret": "test-client-secret",
                    "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
                },
                "database": {
                    "sqlite": {"url": "sqlite:///:memory:"},
                },
                "monitoring": {
                    "enable_analytics": False,
                    "log_level": "INFO",
                },
                "admin_emails": ["admin@example.com"],
            }

        def get(self, key, default=None):
            return self._data.get(key, default)

        def __getitem__(self, key):
            return self._data[key]

        def __contains__(self, key):
            return key in self._data

    # Mock streamlit.secrets
    import streamlit as st

    mock_secrets = MockSecrets()
    monkeypatch.setattr("streamlit.secrets", mock_secrets)

    return mock_secrets
