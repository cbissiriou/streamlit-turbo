"""
Tests unitaires pour le module database
"""

import pytest
from sqlmodel import Session, select

from streamlit_template.database.engine import get_engine, init_db
from streamlit_template.database.models import ActivityLog, DataEntry, User


class TestDatabaseModels:
    """Tests pour les modèles de données"""

    @pytest.fixture(autouse=True)
    def setup_db(self, mock_streamlit_secrets):
        """Setup: Initialise la DB de test avant chaque test"""
        from streamlit_template.database import engine as db_engine

        # Reset le singleton
        db_engine._engine = None

        # Créer les tables
        init_db()

        yield

        # Cleanup
        db_engine._engine = None

    def test_create_user(self):
        """Test: Création d'un utilisateur"""
        engine = get_engine()

        with Session(engine) as session:
            user = User(
                email="test@example.com",
                google_sub="123456",
                name="Test User",
                role="user",
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.role == "user"
            assert user.is_active is True

    def test_user_unique_email(self):
        """Test: L'email doit être unique"""
        engine = get_engine()

        with Session(engine) as session:
            user1 = User(email="duplicate@example.com", google_sub="123", name="User 1")
            user2 = User(email="duplicate@example.com", google_sub="456", name="User 2")

            session.add(user1)
            session.commit()

            session.add(user2)

            with pytest.raises(Exception):  # IntegrityError
                session.commit()

    def test_create_activity_log(self):
        """Test: Création d'un log d'activité"""
        engine = get_engine()

        with Session(engine) as session:
            log = ActivityLog(
                user_email="test@example.com",
                action="page_view",
                page="home",
            )
            session.add(log)
            session.commit()
            session.refresh(log)

            assert log.id is not None
            assert log.action == "page_view"
            assert log.page == "home"

    def test_query_user_by_email(self):
        """Test: Recherche d'utilisateur par email"""
        engine = get_engine()

        with Session(engine) as session:
            # Créer un user
            user = User(email="query@example.com", google_sub="789", name="Query User")
            session.add(user)
            session.commit()

            # Rechercher
            statement = select(User).where(User.email == "query@example.com")
            found_user = session.exec(statement).first()

            assert found_user is not None
            assert found_user.email == "query@example.com"

    def test_data_entry_model(self):
        """Test: Modèle DataEntry"""
        engine = get_engine()

        with Session(engine) as session:
            entry = DataEntry(
                title="Test Entry",
                description="Test description",
                value=42.0,
                category="test",
                owner_email="owner@example.com",
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)

            assert entry.id is not None
            assert entry.title == "Test Entry"
            assert entry.value == 42.0
