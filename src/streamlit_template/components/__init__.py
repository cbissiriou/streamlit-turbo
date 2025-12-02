"""
Composants réutilisables pour l'application Streamlit
"""

from .header import render_header, render_navigation_breadcrumb
from .footer import render_footer, render_footer_minimal
from .sidebar import render_logo_placeholder, render_sidebar_info, render_sidebar_navigation, render_complete_sidebar
from .charts import (
    create_line_chart, create_bar_chart, create_pie_chart, create_scatter_plot,
    create_heatmap, create_gauge_chart, create_waterfall_chart, create_box_plot,
    display_chart_with_controls, create_dashboard_metrics_row, create_comparison_chart,
    create_time_series_chart, create_multi_line_chart, generate_sample_data
)
from .forms import (
    FormBuilder, create_form_field, create_contact_form, create_user_profile_form,
    create_survey_form, create_data_upload_form, create_settings_form,
    create_search_form, display_form_summary, create_wizard_form
)
from .modals import (
    Modal, confirmation_dialog, info_dialog, input_dialog, progress_dialog,
    choice_dialog, file_dialog, custom_dialog, DialogManager, dialog_manager,
    toast_notification, sidebar_modal
)

__all__ = [
    # Header/Footer/Sidebar
    "render_header", "render_navigation_breadcrumb", 
    "render_footer", "render_footer_minimal",
    "render_logo_placeholder", "render_sidebar_info",
    "render_sidebar_navigation", "render_complete_sidebar",
    # Charts
    "create_line_chart", "create_bar_chart", "create_pie_chart", "create_scatter_plot",
    "create_heatmap", "create_gauge_chart", "create_waterfall_chart", "create_box_plot",
    "display_chart_with_controls", "create_dashboard_metrics_row", "create_comparison_chart",
    "create_time_series_chart", "create_multi_line_chart", "generate_sample_data",
    # Forms
    "FormBuilder", "create_form_field", "create_contact_form", "create_user_profile_form",
    "create_survey_form", "create_data_upload_form", "create_settings_form",
    "create_search_form", "display_form_summary", "create_wizard_form",
    # Modals
    "Modal", "confirmation_dialog", "info_dialog", "input_dialog", "progress_dialog",
    "choice_dialog", "file_dialog", "custom_dialog", "DialogManager", "dialog_manager",
    "toast_notification", "sidebar_modal"
]