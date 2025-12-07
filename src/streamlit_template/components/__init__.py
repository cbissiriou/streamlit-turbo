"""
Composants réutilisables pour l'application Streamlit
"""

from .charts import (
    create_bar_chart,
    create_box_plot,
    create_comparison_chart,
    create_dashboard_metrics_row,
    create_gauge_chart,
    create_heatmap,
    create_line_chart,
    create_multi_line_chart,
    create_pie_chart,
    create_scatter_plot,
    create_time_series_chart,
    create_waterfall_chart,
    display_chart_with_controls,
    generate_sample_data,
)
from .footer import render_footer, render_footer_minimal
from .forms import (
    FormBuilder,
    create_contact_form,
    create_data_upload_form,
    create_form_field,
    create_search_form,
    create_settings_form,
    create_survey_form,
    create_user_profile_form,
    create_wizard_form,
    display_form_summary,
)
from .header import render_header, render_navigation_breadcrumb
from .modals import (
    DialogManager,
    Modal,
    choice_dialog,
    confirmation_dialog,
    custom_dialog,
    dialog_manager,
    file_dialog,
    info_dialog,
    input_dialog,
    progress_dialog,
    sidebar_modal,
    toast_notification,
)
from .sidebar import (
    render_complete_sidebar,
    render_logo_placeholder,
    render_sidebar_info,
    render_sidebar_navigation,
)

__all__ = [
    # Header/Footer/Sidebar
    "render_header",
    "render_navigation_breadcrumb",
    "render_footer",
    "render_footer_minimal",
    "render_logo_placeholder",
    "render_sidebar_info",
    "render_sidebar_navigation",
    "render_complete_sidebar",
    # Charts
    "create_line_chart",
    "create_bar_chart",
    "create_pie_chart",
    "create_scatter_plot",
    "create_heatmap",
    "create_gauge_chart",
    "create_waterfall_chart",
    "create_box_plot",
    "display_chart_with_controls",
    "create_dashboard_metrics_row",
    "create_comparison_chart",
    "create_time_series_chart",
    "create_multi_line_chart",
    "generate_sample_data",
    # Forms
    "FormBuilder",
    "create_form_field",
    "create_contact_form",
    "create_user_profile_form",
    "create_survey_form",
    "create_data_upload_form",
    "create_settings_form",
    "create_search_form",
    "display_form_summary",
    "create_wizard_form",
    # Modals
    "Modal",
    "confirmation_dialog",
    "info_dialog",
    "input_dialog",
    "progress_dialog",
    "choice_dialog",
    "file_dialog",
    "custom_dialog",
    "DialogManager",
    "dialog_manager",
    "toast_notification",
    "sidebar_modal",
]
