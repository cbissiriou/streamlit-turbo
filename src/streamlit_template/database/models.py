"""
Modèles de données SQLModel
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    Modèle utilisateur pour stocker les infos complémentaires
    (en plus de l'auth Google OAuth)
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Identifiants OAuth
    email: str = Field(unique=True, index=True)
    google_sub: str = Field(unique=True, index=True)  # Google unique ID

    # Informations profil
    name: Optional[str] = None
    picture_url: Optional[str] = None

    # Rôle et permissions
    role: str = Field(default="user")  # user, admin, etc.
    is_active: bool = Field(default=True)

    # Métadonnées
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

    # Préférences utilisateur (JSON)
    preferences: Optional[str] = None  # Stocké comme JSON string

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "google_sub": "123456789",
                "name": "John Doe",
                "role": "user",
            }
        }


class ActivityLog(SQLModel, table=True):
    """
    Log des activités utilisateurs pour analytics et audit
    """

    __tablename__ = "activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Utilisateur
    user_email: Optional[str] = Field(index=True)

    # Activité
    action: str = Field(index=True)  # page_view, button_click, etc.
    page: Optional[str] = None
    details: Optional[str] = None  # JSON string pour détails additionnels

    # Métadonnées
    timestamp: datetime = Field(default_factory=datetime.now, index=True)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "user@example.com",
                "action": "page_view",
                "page": "dashboard",
                "timestamp": "2024-01-01T12:00:00",
            }
        }


# Exemple de modèle métier (à adapter selon vos besoins)
class DataEntry(SQLModel, table=True):
    """
    Exemple de modèle pour stocker des données métier
    """

    __tablename__ = "data_entries"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Données
    title: str
    description: Optional[str] = None
    value: float = 0.0
    category: Optional[str] = None

    # Ownership
    owner_email: str = Field(index=True)

    # Métadonnées
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Entry",
                "description": "Description here",
                "value": 42.0,
                "owner_email": "user@example.com",
            }
        }
