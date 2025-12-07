"""
Gestionnaire de thèmes pour l'application Streamlit
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import streamlit as st


@dataclass
class ThemeConfig:
    """Configuration d'un thème"""

    name: str
    primary_color: str = "#FF6B6B"
    secondary_color: str = "#4ECDC4"
    accent_color: str = "#45B7D1"
    success_color: str = "#96CEB4"
    warning_color: str = "#FECA57"
    error_color: str = "#FF6B6B"

    text_color: str = "#2C3E50"
    text_light: str = "#7F8C8D"
    background_color: str = "#FFFFFF"
    background_light: str = "#F8F9FA"
    border_color: str = "#E1E8ED"

    font_family: str = "sans-serif"
    font_size_base: int = 14
    border_radius: str = "8px"


# Thèmes prédéfinis
THEMES = {
    "default": ThemeConfig(name="Default", primary_color="#FF6B6B", secondary_color="#4ECDC4"),
    "ocean": ThemeConfig(
        name="Ocean",
        primary_color="#0077BE",
        secondary_color="#00A8CC",
        accent_color="#5DADE2",
        success_color="#58D68D",
        warning_color="#F7DC6F",
        error_color="#EC7063",
    ),
    "forest": ThemeConfig(
        name="Forest",
        primary_color="#27AE60",
        secondary_color="#2ECC71",
        accent_color="#58D68D",
        success_color="#A9DFBF",
        warning_color="#F4D03F",
        error_color="#E74C3C",
    ),
    "sunset": ThemeConfig(
        name="Sunset",
        primary_color="#E67E22",
        secondary_color="#F39C12",
        accent_color="#F8C471",
        success_color="#82E0AA",
        warning_color="#F7DC6F",
        error_color="#E74C3C",
    ),
    "purple": ThemeConfig(
        name="Purple",
        primary_color="#8E44AD",
        secondary_color="#9B59B6",
        accent_color="#BB8FCE",
        success_color="#82E0AA",
        warning_color="#F7DC6F",
        error_color="#E74C3C",
    ),
    "dark": ThemeConfig(
        name="Dark",
        primary_color="#3498DB",
        secondary_color="#E74C3C",
        accent_color="#F39C12",
        text_color="#FFFFFF",
        text_light="#BDC3C7",
        background_color="#2C3E50",
        background_light="#34495E",
        border_color="#485563",
    ),
    "minimal": ThemeConfig(
        name="Minimal",
        primary_color="#2C3E50",
        secondary_color="#95A5A6",
        accent_color="#3498DB",
        success_color="#27AE60",
        warning_color="#F39C12",
        error_color="#E74C3C",
        background_light="#FAFAFA",
    ),
}


class ThemeManager:
    """Gestionnaire de thèmes pour l'application"""

    def __init__(self):
        self.current_theme = "default"
        self.styles_dir = Path(__file__).parent

    def get_available_themes(self) -> dict[str, str]:
        """Retourne la liste des thèmes disponibles"""
        return {key: theme.name for key, theme in THEMES.items()}

    def get_current_theme(self) -> str:
        """Retourne le thème actuel"""
        return st.session_state.get("current_theme", self.current_theme)

    def set_theme(self, theme_name: str):
        """Définit le thème actuel"""
        if theme_name in THEMES:
            st.session_state.current_theme = theme_name
            self.current_theme = theme_name
        else:
            raise ValueError(f"Thème '{theme_name}' non trouvé")

    def get_theme_config(self, theme_name: str | None = None) -> ThemeConfig:
        """Retourne la configuration d'un thème"""
        if theme_name is None:
            theme_name = self.get_current_theme()

        return THEMES.get(theme_name, THEMES["default"])

    def generate_css_variables(self, theme_name: str | None = None) -> str:
        """Génère les variables CSS pour un thème"""
        config = self.get_theme_config(theme_name)

        return f"""
        :root {{
            --primary-color: {config.primary_color};
            --secondary-color: {config.secondary_color};
            --accent-color: {config.accent_color};
            --success-color: {config.success_color};
            --warning-color: {config.warning_color};
            --error-color: {config.error_color};

            --text-color: {config.text_color};
            --text-light: {config.text_light};
            --background-color: {config.background_color};
            --background-light: {config.background_light};
            --border-color: {config.border_color};

            --font-family: {config.font_family};
            --font-size-base: {config.font_size_base}px;
            --border-radius: {config.border_radius};
        }}
        """

    def apply_theme(self, theme_name: str | None = None):
        """Applique un thème à l'application"""
        if theme_name:
            self.set_theme(theme_name)

        # Génère le CSS du thème
        css_variables = self.generate_css_variables()

        # Charge les styles de base
        main_css = self.load_css_file("main.css")
        components_css = self.load_css_file("components.css")

        # Combine tout le CSS
        full_css = f"""
        <style>
        {css_variables}
        {main_css}
        {components_css}
        </style>
        """

        # Applique le CSS
        st.markdown(full_css, unsafe_allow_html=True)

    def load_css_file(self, filename: str) -> str:
        """Charge un fichier CSS"""
        css_path = self.styles_dir / filename

        if css_path.exists():
            return css_path.read_text()
        else:
            st.warning(f"Fichier CSS non trouvé: {filename}")
            return ""

    def create_theme_selector(self) -> str:
        """Crée un sélecteur de thème dans la sidebar"""
        current = self.get_current_theme()
        themes = self.get_available_themes()

        selected = st.sidebar.selectbox(
            "🎨 Thème",
            options=list(themes.keys()),
            format_func=lambda x: themes[x],
            index=list(themes.keys()).index(current) if current in themes else 0,
            help="Choisissez un thème pour l'application",
        )

        if selected != current:
            self.apply_theme(selected)
            st.rerun()

        return selected

    def create_custom_theme_editor(self):
        """Crée un éditeur de thème personnalisé"""
        st.subheader("🎨 Créateur de thème personnalisé")

        current_config = self.get_theme_config()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Couleurs principales")
            primary = st.color_picker("Couleur principale", current_config.primary_color)
            secondary = st.color_picker("Couleur secondaire", current_config.secondary_color)
            accent = st.color_picker("Couleur d'accent", current_config.accent_color)

        with col2:
            st.markdown("#### Couleurs d'état")
            success = st.color_picker("Succès", current_config.success_color)
            warning = st.color_picker("Avertissement", current_config.warning_color)
            error = st.color_picker("Erreur", current_config.error_color)

        # Aperçu du thème
        st.markdown("#### Aperçu")
        preview_css = f"""
        <div style="
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
        ">
            <h3>Aperçu du thème personnalisé</h3>
            <p>Couleur principale: {primary}</p>
            <p>Couleur secondaire: {secondary}</p>
        </div>

        <div style="display: flex; gap: 1rem; margin: 1rem 0;">
            <div style="background: {success}; padding: 1rem; border-radius: 8px; color: white;">
                Succès
            </div>
            <div style="background: {warning}; padding: 1rem; border-radius: 8px; color: white;">
                Avertissement
            </div>
            <div style="background: {error}; padding: 1rem; border-radius: 8px; color: white;">
                Erreur
            </div>
        </div>
        """

        st.markdown(preview_css, unsafe_allow_html=True)

        # Sauvegarde du thème personnalisé
        theme_name = st.text_input("Nom du thème personnalisé", "mon_theme")

        if st.button("💾 Sauvegarder le thème"):
            custom_theme = ThemeConfig(
                name=theme_name.title(),
                primary_color=primary,
                secondary_color=secondary,
                accent_color=accent,
                success_color=success,
                warning_color=warning,
                error_color=error,
            )

            # Ajoute le thème aux thèmes disponibles
            THEMES[theme_name.lower()] = custom_theme

            st.success(f"Thème '{theme_name}' sauvegardé!")
            st.info("Le thème sera disponible dans le sélecteur après redémarrage.")

    def export_theme(self, theme_name: str | None = None) -> dict[str, Any]:
        """Exporte un thème au format JSON"""
        config = self.get_theme_config(theme_name)

        return {
            "name": config.name,
            "colors": {
                "primary": config.primary_color,
                "secondary": config.secondary_color,
                "accent": config.accent_color,
                "success": config.success_color,
                "warning": config.warning_color,
                "error": config.error_color,
            },
            "text": {"color": config.text_color, "light": config.text_light},
            "background": {
                "main": config.background_color,
                "light": config.background_light,
                "border": config.border_color,
            },
            "typography": {"font_family": config.font_family, "font_size": config.font_size_base},
            "ui": {"border_radius": config.border_radius},
        }

    def import_theme(self, theme_data: dict[str, Any], theme_key: str):
        """Importe un thème depuis un dictionnaire"""
        try:
            colors = theme_data.get("colors", {})
            text = theme_data.get("text", {})
            background = theme_data.get("background", {})
            typography = theme_data.get("typography", {})
            ui = theme_data.get("ui", {})

            imported_theme = ThemeConfig(
                name=theme_data.get("name", "Imported Theme"),
                primary_color=colors.get("primary", "#FF6B6B"),
                secondary_color=colors.get("secondary", "#4ECDC4"),
                accent_color=colors.get("accent", "#45B7D1"),
                success_color=colors.get("success", "#96CEB4"),
                warning_color=colors.get("warning", "#FECA57"),
                error_color=colors.get("error", "#FF6B6B"),
                text_color=text.get("color", "#2C3E50"),
                text_light=text.get("light", "#7F8C8D"),
                background_color=background.get("main", "#FFFFFF"),
                background_light=background.get("light", "#F8F9FA"),
                border_color=background.get("border", "#E1E8ED"),
                font_family=typography.get("font_family", "sans-serif"),
                font_size_base=typography.get("font_size", 14),
                border_radius=ui.get("border_radius", "8px"),
            )

            THEMES[theme_key] = imported_theme
            return True

        except Exception as e:
            st.error(f"Erreur lors de l'import du thème: {e}")
            return False


# Instance globale du gestionnaire de thèmes
theme_manager = ThemeManager()


def apply_theme(theme_name: str = "default"):
    """Fonction utilitaire pour appliquer un thème"""
    theme_manager.apply_theme(theme_name)


def get_current_theme() -> str:
    """Fonction utilitaire pour récupérer le thème actuel"""
    return theme_manager.get_current_theme()


def create_theme_selector() -> str:
    """Fonction utilitaire pour créer un sélecteur de thème"""
    return theme_manager.create_theme_selector()
