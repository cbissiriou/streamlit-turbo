"""
Module core - Fonctionnalités centrales de l'application
"""

from .config import AppConfig, get_config, update_config
from .state_manager import (
    AppState, get_state, update_state, reset_state,
    set_current_page, add_notification, clear_notifications,
    set_error, clear_error, cache_data, get_cached_data, clear_cache
)
from .cache_manager import (
    CacheManager, cached_function, st_cached_data,
    clear_all_cache, get_cache_stats
)
from .validators import (
    ValidationError, Validator, RequiredValidator, EmailValidator,
    LengthValidator, NumericRangeValidator, RegexValidator,
    FileExtensionValidator, validate_form_data, display_validation_errors,
    COMMON_VALIDATORS
)

__all__ = [
    # Config
    "AppConfig", "get_config", "update_config",
    # State Management
    "AppState", "get_state", "update_state", "reset_state",
    "set_current_page", "add_notification", "clear_notifications",
    "set_error", "clear_error", "cache_data", "get_cached_data", "clear_cache",
    # Cache Management
    "CacheManager", "cached_function", "st_cached_data",
    "clear_all_cache", "get_cache_stats",
    # Validation
    "ValidationError", "Validator", "RequiredValidator", "EmailValidator",
    "LengthValidator", "NumericRangeValidator", "RegexValidator",
    "FileExtensionValidator", "validate_form_data", "display_validation_errors",
    "COMMON_VALIDATORS"
]
