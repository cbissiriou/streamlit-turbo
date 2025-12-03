"""
Module utils - Utilitaires et fonctions d'aide
"""

from .data_loader import get_data_summary, load_sample_data
from .decorators import (
    cache_result,
    handle_errors,
    log_function_call,
    measure_time,
    require_authentication,
    retry,
    streamlit_fragment,
    validate_inputs,
    with_spinner,
)
from .helpers import (
    calculate_percentage_change,
    clean_dataframe,
    create_download_link,
    create_info_box,
    df_to_download_link,
    display_metric_card,
    format_currency,
    format_datetime,
    format_number,
    format_percentage,
    get_color_scale,
    json_pretty_print,
    main_spacer,
    safe_divide,
    sidebar_spacer,
    truncate_text,
)
from .logger import (
    ColoredFormatter,
    StreamlitLogHandler,
    clear_logs,
    display_log_viewer,
    get_logger,
    init_default_logger,
    log_data_operation,
    log_function_execution,
    log_user_action,
    setup_logging,
)

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
