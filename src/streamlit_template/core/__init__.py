"""
Module core - Fonctionnalités centrales de l'application
"""

from .cache_manager import (
    CacheManager,
    cached_function,
    clear_all_cache,
    get_cache_stats,
    st_cached_data,
)
from .config import AppConfig, get_config, update_config
from .state_manager import (
    AppState,
    add_notification,
    cache_data,
    clear_cache,
    clear_error,
    clear_notifications,
    get_cached_data,
    get_state,
    reset_state,
    set_current_page,
    set_error,
    update_state,
)
from .validators import (
    COMMON_VALIDATORS,
    EmailValidator,
    FileExtensionValidator,
    LengthValidator,
    NumericRangeValidator,
    RegexValidator,
    RequiredValidator,
    ValidationError,
    Validator,
    display_validation_errors,
    validate_form_data,
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
