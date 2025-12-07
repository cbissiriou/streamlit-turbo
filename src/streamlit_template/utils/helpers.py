"""
Fonctions utilitaires générales
"""

import base64
import json
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st


def format_number(value: int | float, precision: int = 2, suffix: str = "") -> str:
    """Formate un nombre avec séparateurs et suffixe"""
    if value >= 1e9:
        return f"{value / 1e9:.{precision}f}B{suffix}"
    elif value >= 1e6:
        return f"{value / 1e6:.{precision}f}M{suffix}"
    elif value >= 1e3:
        return f"{value / 1e3:.{precision}f}K{suffix}"
    else:
        return f"{value:.{precision}f}{suffix}"


def format_percentage(value: float, precision: int = 1) -> str:
    """Formate un nombre en pourcentage"""
    return f"{value:.{precision}f}%"


def format_currency(value: float, currency: str = "€", precision: int = 2) -> str:
    """Formate un montant en devise"""
    return f"{value:,.{precision}f} {currency}"


def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """Formate une datetime en string"""
    return dt.strftime(format_str)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calcule le pourcentage de changement entre deux valeurs"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    return ((new_value - old_value) / old_value) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Division sécurisée qui évite la division par zéro"""
    return numerator / denominator if denominator != 0 else default


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Tronque un texte à une longueur maximale"""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def create_download_link(
    data: str | bytes | pd.DataFrame, filename: str, mime_type: str = "text/plain"
) -> str:
    """Crée un lien de téléchargement pour des données"""

    if isinstance(data, pd.DataFrame):
        if filename.endswith(".csv"):
            data = data.to_csv(index=False)
            mime_type = "text/csv"
        elif filename.endswith(".json"):
            data = data.to_json(orient="records", indent=2)
            mime_type = "application/json"

    if isinstance(data, str):
        data = data.encode()

    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">{filename}</a>'
    return href


def df_to_download_link(df: pd.DataFrame, filename: str, format_type: str = "csv") -> str:
    """Convertit un DataFrame en lien de téléchargement"""
    if format_type.lower() == "csv":
        csv = df.to_csv(index=False)
        return create_download_link(csv, filename, "text/csv")
    elif format_type.lower() == "json":
        json_str = df.to_json(orient="records", indent=2)
        return create_download_link(json_str, filename, "application/json")
    else:
        raise ValueError("Format supporté: csv, json")


def clean_dataframe(df: pd.DataFrame, remove_duplicates: bool = True) -> pd.DataFrame:
    """Nettoie un DataFrame (valeurs nulles, doublons, etc.)"""
    # Copie pour ne pas modifier l'original
    cleaned_df = df.copy()

    # Supprime les lignes entièrement vides
    cleaned_df = cleaned_df.dropna(how="all")

    # Supprime les colonnes entièrement vides
    cleaned_df = cleaned_df.dropna(axis=1, how="all")

    # Supprime les doublons si demandé
    if remove_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df


def get_color_scale(value: float, min_val: float, max_val: float, colors: list[str] = None) -> str:
    """Retourne une couleur basée sur une échelle de valeurs"""
    if colors is None:
        colors = ["#ff4444", "#ffaa44", "#44ff44"]  # Rouge -> Orange -> Vert

    if max_val == min_val:
        return colors[len(colors) // 2]  # Couleur du milieu

    # Normalise la valeur entre 0 et 1
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))  # Clamp entre 0 et 1

    # Trouve l'index de couleur
    color_index = int(normalized * (len(colors) - 1))
    return colors[color_index]


def display_metric_card(
    title: str, value: Any, delta: float | None = None, format_func: callable = str
):
    """Affiche une carte de métrique stylée"""
    formatted_value = format_func(value)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.metric(
            label=title,
            value=formatted_value,
            delta=f"{delta:+.1f}%" if delta is not None else None,
        )


def create_info_box(title: str, content: str, type: str = "info"):
    """Crée une boîte d'information colorée"""
    icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}

    icon = icons.get(type, "ℹ️")
    st.markdown(
        f"""
    <div style="
        padding: 1rem;
        border-left: 4px solid #007bff;
        background-color: #f8f9fa;
        border-radius: 4px;
        margin: 1rem 0;
    ">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def sidebar_spacer(height: int = 20):
    """Ajoute un espace vertical dans la sidebar"""
    st.sidebar.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)


def main_spacer(height: int = 20):
    """Ajoute un espace vertical dans le contenu principal"""
    st.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)


def json_pretty_print(data: dict[str, Any], max_height: int = 300):
    """Affiche du JSON de manière formatée"""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    st.code(json_str, language="json")
