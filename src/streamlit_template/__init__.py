"""
Streamlit Template - Package principal
Architecture modulaire pour applications Streamlit professionnelles
"""

from .core import (
    AppConfig, get_config, update_config,
    AppState, get_state, update_state, reset_state,
    set_current_page, add_notification, clear_notifications,
    set_error, clear_error, cache_data, get_cached_data, clear_cache,
    CacheManager, cached_function, st_cached_data, 
    clear_all_cache, get_cache_stats,
    ValidationError, Validator, RequiredValidator, EmailValidator,
    LengthValidator, NumericRangeValidator, RegexValidator,
    FileExtensionValidator, validate_form_data, display_validation_errors,
    COMMON_VALIDATORS
)

from .components import (
    render_header, render_navigation_breadcrumb, 
    render_footer, render_footer_minimal,
    render_logo_placeholder, render_sidebar_info,
    render_sidebar_navigation, render_complete_sidebar,
    create_line_chart, create_bar_chart, create_pie_chart, create_scatter_plot,
    create_heatmap, create_gauge_chart, create_waterfall_chart, create_box_plot,
    display_chart_with_controls, create_dashboard_metrics_row, create_comparison_chart,
    create_time_series_chart, generate_sample_data,
    FormBuilder, create_form_field, create_contact_form, create_user_profile_form,
    create_survey_form, create_data_upload_form, create_settings_form,
    create_search_form, display_form_summary, create_wizard_form,
    Modal, confirmation_dialog, info_dialog, input_dialog, progress_dialog,
    choice_dialog, file_dialog, custom_dialog, DialogManager, dialog_manager,
    toast_notification, sidebar_modal
)

from .utils import (
    format_number, format_percentage, format_currency, format_datetime,
    calculate_percentage_change, safe_divide, truncate_text,
    create_download_link, df_to_download_link, clean_dataframe,
    get_color_scale, display_metric_card, create_info_box,
    sidebar_spacer, main_spacer, json_pretty_print,
    measure_time, with_spinner, handle_errors, require_authentication,
    cache_result, log_function_call, validate_inputs, streamlit_fragment, retry,
    StreamlitLogHandler, ColoredFormatter, setup_logging, get_logger,
    log_function_execution, log_user_action, log_data_operation,
    display_log_viewer, clear_logs, init_default_logger,
    load_sample_data, get_data_summary
)

from .styles import (
    ThemeConfig, ThemeManager, THEMES, theme_manager,
    apply_theme, get_current_theme, create_theme_selector
)

# Informations sur le package
__version__ = "0.1.0"
__author__ = "Streamlit Template"
__description__ = "Template Streamlit avec architecture modulaire et professionnelle"

# Exports principaux
__all__ = [
    # Version info
    "__version__", "__author__", "__description__",
    
    # Core - Configuration
    "AppConfig", "get_config", "update_config",
    
    # Core - State Management  
    "AppState", "get_state", "update_state", "reset_state",
    "set_current_page", "add_notification", "clear_notifications",
    "set_error", "clear_error", "cache_data", "get_cached_data", "clear_cache",
    
    # Core - Cache Management
    "CacheManager", "cached_function", "st_cached_data", 
    "clear_all_cache", "get_cache_stats",
    
    # Core - Validation
    "ValidationError", "Validator", "RequiredValidator", "EmailValidator",
    "LengthValidator", "NumericRangeValidator", "RegexValidator",
    "FileExtensionValidator", "validate_form_data", "display_validation_errors",
    "COMMON_VALIDATORS",
    
    # Components - Layout
    "render_header", "render_navigation_breadcrumb", 
    "render_footer", "render_footer_minimal",
    "render_logo_placeholder", "render_sidebar_info",
    "render_sidebar_navigation", "render_complete_sidebar",
    
    # Components - Charts
    "create_line_chart", "create_bar_chart", "create_pie_chart", "create_scatter_plot",
    "create_heatmap", "create_gauge_chart", "create_waterfall_chart", "create_box_plot",
    "display_chart_with_controls", "create_dashboard_metrics_row", "create_comparison_chart",
    "create_time_series_chart", "generate_sample_data",
    
    # Components - Forms
    "FormBuilder", "create_form_field", "create_contact_form", "create_user_profile_form",
    "create_survey_form", "create_data_upload_form", "create_settings_form",
    "create_search_form", "display_form_summary", "create_wizard_form",
    
    # Components - Modals
    "Modal", "confirmation_dialog", "info_dialog", "input_dialog", "progress_dialog",
    "choice_dialog", "file_dialog", "custom_dialog", "DialogManager", "dialog_manager",
    "toast_notification", "sidebar_modal",

    # Utils - Formatting
    "format_number", "format_percentage", "format_currency", "format_datetime",
    "calculate_percentage_change", "safe_divide", "truncate_text",

    # Utils - Data
    "create_download_link", "df_to_download_link", "clean_dataframe",
    "load_sample_data", "get_data_summary",
    
    # Utils - UI
    "get_color_scale", "display_metric_card", "create_info_box",
    "sidebar_spacer", "main_spacer", "json_pretty_print",
    
    # Utils - Decorators
    "measure_time", "with_spinner", "handle_errors", "require_authentication",
    "cache_result", "log_function_call", "validate_inputs", "streamlit_fragment", "retry",
    
    # Utils - Logging
    "StreamlitLogHandler", "ColoredFormatter", "setup_logging", "get_logger",
    "log_function_execution", "log_user_action", "log_data_operation",
    "display_log_viewer", "clear_logs", "init_default_logger",
    
    # Styles
    "ThemeConfig", "ThemeManager", "THEMES", "theme_manager",
    "apply_theme", "get_current_theme", "create_theme_selector",
]

# Initialisation par défaut
def init_app():
    """Initialise l'application avec les paramètres par défaut"""
    # Initialise la configuration
    get_config()
    
    # Initialise l'état
    get_state()
    
    # Initialise le logger
    init_default_logger()
    
    # Applique le thème par défaut
    apply_theme()

# Message de bienvenue
def welcome_message():
    """Affiche le message de bienvenue"""
    return f"""
    🚀 **Streamlit Template v{__version__}**
    
    Template professionnel avec architecture modulaire pour vos applications Streamlit.
    
    **Fonctionnalités incluses :**
    - 🏗️ Architecture modulaire (core, components, pages, utils, styles)
    - ⚙️ Configuration centralisée et gestion d'état
    - 🎨 Système de thèmes et composants réutilisables
    - 📊 Composants de graphiques avancés (Plotly)
    - 📝 Formulaires avec validation
    - 💾 Cache intelligent et optimisations
    - 📋 Système de logging complet
    - 🛠️ Utilitaires et décorateurs
    
    **Usage rapide :**
    ```python
    import streamlit_template as st_template
    
    # Initialise l'application
    st_template.init_app()
    
    # Utilise les composants
    st_template.render_header("Mon App")
    # ... votre contenu
    st_template.render_footer()
    ```
    """

# Auto-initialisation si appelé directement
if __name__ == "__main__":
    print(welcome_message())