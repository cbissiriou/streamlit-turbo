"""
Gestionnaire de cache avancé pour Streamlit
"""

import hashlib
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from typing import Any

import streamlit as st


class CacheManager:
    """Gestionnaire de cache personnalisé"""

    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._cache: dict[str, dict] = {}

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Génère une clé unique pour la fonction et ses arguments"""
        key_data = (func_name, args, sorted(kwargs.items()))
        key_str = str(key_data)
        return hashlib.md5(key_str.encode()).hexdigest()

    def _is_expired(self, cache_entry: dict) -> bool:
        """Vérifie si l'entrée de cache a expiré"""
        if "expires_at" not in cache_entry:
            return False
        return datetime.now() > cache_entry["expires_at"]

    def get(self, key: str) -> Any | None:
        """Récupère une valeur du cache"""
        if key in self._cache:
            entry = self._cache[key]
            if not self._is_expired(entry):
                return entry["value"]
            else:
                # Supprime l'entrée expirée
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Stocke une valeur dans le cache"""
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)

        self._cache[key] = {
            "value": value,
            "created_at": datetime.now(),
            "expires_at": expires_at
        }

    def invalidate(self, key: str) -> None:
        """Supprime une entrée du cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Vide tout le cache"""
        self._cache.clear()

    def size(self) -> int:
        """Retourne la taille du cache"""
        return len(self._cache)

    def cleanup_expired(self) -> int:
        """Nettoie les entrées expirées et retourne le nombre supprimé"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if self._is_expired(entry)
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)


# Instance globale du cache
_cache_manager = CacheManager()


def cached_function(ttl: int = 3600, key_prefix: str = ""):
    """
    Décorateur pour mettre en cache les résultats de fonction
    
    Args:
        ttl: Temps de vie en secondes
        key_prefix: Préfixe pour la clé de cache
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Génère la clé de cache
            cache_key = _cache_manager._generate_key(
                f"{key_prefix}_{func.__name__}",
                args,
                kwargs
            )

            # Vérifie le cache
            cached_result = _cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Exécute la fonction et met en cache
            result = func(*args, **kwargs)
            _cache_manager.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator


def st_cached_data(func: Callable = None, *, ttl: int = 3600, show_spinner: str = "Loading..."):
    """
    Version simplifiée du cache Streamlit avec gestion d'erreur
    """
    def decorator(f):
        @st.cache_data(ttl=ttl, show_spinner=show_spinner)
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                st.error(f"Erreur lors du chargement des données: {str(e)}")
                return None
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def clear_all_cache():
    """Vide tous les caches (Streamlit + custom)"""
    st.cache_data.clear()
    _cache_manager.clear()


def get_cache_stats() -> dict[str, Any]:
    """Retourne les statistiques du cache"""
    return {
        "cache_size": _cache_manager.size(),
        "expired_cleaned": _cache_manager.cleanup_expired()
    }
