"""
Module utils - Utilitaires et fonctions d'aide
"""

from .helpers import (
    format_number, format_percentage, format_currency, format_datetime,
    calculate_percentage_change, safe_divide, truncate_text,
    create_download_link, df_to_download_link, clean_dataframe,
    get_color_scale, display_metric_card, create_info_box,
    sidebar_spacer, main_spacer, json_pretty_print
)
from .decorators import (
    measure_time, with_spinner, handle_errors, require_authentication,
    cache_result, log_function_call, validate_inputs, streamlit_fragment, retry
)
from .logger import (
    StreamlitLogHandler, ColoredFormatter, setup_logging, get_logger,
    log_function_execution, log_user_action, log_data_operation,
    display_log_viewer, clear_logs, init_default_logger
)
from .data_loader import load_sample_data, get_data_summary

__all__ = [
    # Helpers
    "format_number", "format_percentage", "format_currency", "format_datetime",
    "calculate_percentage_change", "safe_divide", "truncate_text",
    "create_download_link", "df_to_download_link", "clean_dataframe",
    "get_color_scale", "display_metric_card", "create_info_box",
    "sidebar_spacer", "main_spacer", "json_pretty_print",
    # Decorators
    "measure_time", "with_spinner", "handle_errors", "require_authentication",
    "cache_result", "log_function_call", "validate_inputs", "streamlit_fragment", "retry",
    # Logger
    "StreamlitLogHandler", "ColoredFormatter", "setup_logging", "get_logger",
    "log_function_execution", "log_user_action", "log_data_operation",
    "display_log_viewer", "clear_logs", "init_default_logger",
    # Data Loader
    "load_sample_data", "get_data_summary"
]