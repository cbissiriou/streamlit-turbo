"""
Composants de graphiques réutilisables avec Plotly
"""

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_line_chart(
    data: pd.DataFrame, x: str, y: str, title: str = "", color: str | None = None, height: int = 400
) -> go.Figure:
    """
    Crée un graphique linéaire stylé

    Args:
        data: DataFrame avec les données
        x: Nom de la colonne X
        y: Nom de la colonne Y
        title: Titre du graphique
        color: Colonne pour les couleurs (optionnel)
        height: Hauteur du graphique
    """
    if color:
        fig = px.line(data, x=x, y=y, color=color, title=title)
    else:
        fig = px.line(data, x=x, y=y, title=title)

    # Styling personnalisé
    fig.update_layout(
        height=height,
        showlegend=True if color else False,
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
        title=dict(x=0.5, font=dict(size=16, color="#2C3E50")),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128,128,128,0.2)",
            showline=True,
            linewidth=1,
            linecolor="rgba(128,128,128,0.5)",
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128,128,128,0.2)",
            showline=True,
            linewidth=1,
            linecolor="rgba(128,128,128,0.5)",
        ),
    )

    # Couleurs personnalisées
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]
    if not color and len(fig.data) == 1:
        fig.update_traces(line=dict(color=colors[0], width=3))

    return fig


def create_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    orientation: str = "v",
    color: str | None = None,
    height: int = 400,
) -> go.Figure:
    """
    Crée un graphique en barres stylé
    """
    if color:
        fig = px.bar(data, x=x, y=y, color=color, title=title, orientation=orientation)
    else:
        fig = px.bar(data, x=x, y=y, title=title, orientation=orientation)

    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(x=0.5, font=dict(size=16, color="#2C3E50")),
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)"),
    )

    # Gradient pour les barres
    if not color:
        fig.update_traces(
            marker=dict(color="#FF6B6B", line=dict(color="rgba(128,128,128,0.5)", width=1))
        )

    return fig


def create_pie_chart(
    data: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    hole: float = 0.0,
    height: int = 400,
) -> go.Figure:
    """
    Crée un graphique en secteurs (ou donut) stylé
    """
    fig = px.pie(data, values=values, names=names, title=title, hole=hole)

    # Couleurs personnalisées
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#A8E6CF", "#FFB6C1"]

    fig.update_layout(
        height=height,
        showlegend=True,
        legend=dict(orientation="v", x=1.05, y=0.5),
        title=dict(x=0.5, font=dict(size=16, color="#2C3E50")),
    )

    fig.update_traces(
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textposition="inside",
        textinfo="percent+label",
    )

    return fig


def create_scatter_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    size: str | None = None,
    color: str | None = None,
    height: int = 400,
) -> go.Figure:
    """
    Crée un nuage de points stylé
    """
    fig = px.scatter(data, x=x, y=y, size=size, color=color, title=title)

    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(x=0.5, font=dict(size=16, color="#2C3E50")),
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)"),
    )

    return fig


def create_heatmap(
    data: pd.DataFrame, title: str = "", height: int = 400, colorscale: str = "Viridis"
) -> go.Figure:
    """
    Crée une heatmap stylée
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=data.values, x=data.columns, y=data.index, colorscale=colorscale, showscale=True
        )
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#2C3E50")),
        height=height,
        xaxis=dict(side="bottom"),
        yaxis=dict(side="left"),
    )

    return fig


def create_gauge_chart(
    value: float,
    min_val: float = 0,
    max_val: float = 100,
    title: str = "",
    unit: str = "",
    height: int = 300,
) -> go.Figure:
    """
    Crée un gauge (jauge) stylé
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
            delta={"reference": max_val * 0.8},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": "#FF6B6B"},
                "steps": [
                    {"range": [min_val, max_val * 0.3], "color": "lightgray"},
                    {"range": [max_val * 0.3, max_val * 0.7], "color": "gray"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": max_val * 0.9,
                },
            },
        )
    )

    fig.update_layout(
        height=height,
        font={"color": "#2C3E50", "family": "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_waterfall_chart(
    categories: list[str], values: list[float], title: str = "", height: int = 400
) -> go.Figure:
    """
    Crée un graphique waterfall (cascade)
    """
    fig = go.Figure(
        go.Waterfall(
            name="Waterfall",
            orientation="v",
            measure=["relative"] * (len(values) - 1) + ["total"],
            x=categories,
            textposition="outside",
            text=[f"+{v}" if v > 0 else str(v) for v in values],
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#4ECDC4"}},
            decreasing={"marker": {"color": "#FF6B6B"}},
            totals={"marker": {"color": "#45B7D1"}},
        )
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#2C3E50")),
        height=height,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_box_plot(
    data: pd.DataFrame, y: str, x: str | None = None, title: str = "", height: int = 400
) -> go.Figure:
    """
    Crée un box plot stylé
    """
    if x:
        fig = px.box(data, x=x, y=y, title=title)
    else:
        fig = px.box(data, y=y, title=title)

    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(x=0.5, font=dict(size=16, color="#2C3E50")),
    )

    fig.update_traces(marker_color="#FF6B6B", line_color="#2C3E50")

    return fig


def display_chart_with_controls(chart_func: callable, data: pd.DataFrame, **kwargs):
    """
    Affiche un graphique avec des contrôles interactifs
    """
    st.markdown("#### Contrôles du graphique")

    col1, col2, col3 = st.columns(3)

    with col1:
        height = st.slider("Hauteur", 300, 800, 400)

    with col2:
        show_toolbar = st.checkbox("Barre d'outils", True)

    with col3:
        download = st.checkbox("Téléchargeable", True)

    # Crée et affiche le graphique
    fig = chart_func(data, height=height, **kwargs)

    config = {
        "displayModeBar": show_toolbar,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
    }

    if download:
        config["toImageButtonOptions"] = {
            "format": "png",
            "filename": "chart",
            "height": height,
            "width": 800,
            "scale": 1,
        }

    st.plotly_chart(fig, use_container_width=True, config=config)


def create_dashboard_metrics_row(metrics: dict[str, Any]):
    """
    Crée une ligne de métriques pour un dashboard

    Args:
        metrics: Dict avec {nom: {value, delta, format_func}}
    """
    cols = st.columns(len(metrics))

    for i, (name, metric_data) in enumerate(metrics.items()):
        with cols[i]:
            value = metric_data.get("value", 0)
            delta = metric_data.get("delta", None)
            format_func = metric_data.get("format_func", str)

            st.metric(
                label=name,
                value=format_func(value),
                delta=f"{delta:+.1f}%" if delta is not None else None,
            )


def create_comparison_chart(
    data: pd.DataFrame,
    categories: list[str],
    values: list[str],
    title: str = "",
    chart_type: str = "bar",
) -> go.Figure:
    """
    Crée un graphique de comparaison multi-séries
    """
    fig = go.Figure()

    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]

    for i, value_col in enumerate(values):
        if chart_type == "bar":
            fig.add_trace(
                go.Bar(
                    x=data[categories[0]],
                    y=data[value_col],
                    name=value_col,
                    marker_color=colors[i % len(colors)],
                )
            )
        elif chart_type == "line":
            fig.add_trace(
                go.Scatter(
                    x=data[categories[0]],
                    y=data[value_col],
                    mode="lines+markers",
                    name=value_col,
                    line=dict(color=colors[i % len(colors)], width=3),
                )
            )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#2C3E50")),
        barmode="group" if chart_type == "bar" else None,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_time_series_chart(
    data: pd.DataFrame,
    date_col: str,
    value_cols: list[str],
    title: str = "",
    show_range_selector: bool = True,
) -> go.Figure:
    """
    Crée un graphique de série temporelle avec sélecteur de plage
    """
    fig = go.Figure()

    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]

    for i, col in enumerate(value_cols):
        fig.add_trace(
            go.Scatter(
                x=data[date_col],
                y=data[col],
                mode="lines",
                name=col,
                line=dict(color=colors[i % len(colors)], width=2),
            )
        )

    if show_range_selector:
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=7, label="7j", step="day", stepmode="backward"),
                            dict(count=30, label="30j", step="day", stepmode="backward"),
                            dict(count=90, label="3M", step="day", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#2C3E50")),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def create_multi_line_chart(
    data: pd.DataFrame, x: str, y_columns: list[str], title: str = "", height: int = 400
) -> go.Figure:
    """
    Crée un graphique multi-lignes avec plusieurs séries sur le même axe X

    Args:
        data: DataFrame avec les données
        x: Nom de la colonne X
        y_columns: Liste des noms de colonnes Y à afficher
        title: Titre du graphique
        height: Hauteur du graphique
    """
    fig = go.Figure()

    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]

    for i, y_col in enumerate(y_columns):
        fig.add_trace(
            go.Scatter(
                x=data[x],
                y=data[y_col],
                mode="lines+markers",
                name=y_col,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=4),
            )
        )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#2C3E50")),
        height=height,
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128,128,128,0.2)",
            showline=True,
            linewidth=1,
            linecolor="rgba(128,128,128,0.5)",
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128,128,128,0.2)",
            showline=True,
            linewidth=1,
            linecolor="rgba(128,128,128,0.5)",
        ),
    )

    return fig


def generate_sample_data(chart_type: str = "line") -> pd.DataFrame:
    """Génère des données d'exemple pour les graphiques"""
    np.random.seed(42)

    if chart_type == "line":
        dates = pd.date_range(start="2024-01-01", periods=90, freq="D")
        data = pd.DataFrame(
            {
                "date": dates,
                "value": np.cumsum(np.random.randn(90) * 10) + 1000,
                "value2": np.cumsum(np.random.randn(90) * 8) + 800,
            }
        )

    elif chart_type == "bar":
        categories = ["A", "B", "C", "D", "E"]
        data = pd.DataFrame(
            {
                "category": categories,
                "value": np.random.randint(10, 100, len(categories)),
                "value2": np.random.randint(5, 80, len(categories)),
            }
        )

    elif chart_type == "pie":
        categories = ["Segment A", "Segment B", "Segment C", "Segment D"]
        data = pd.DataFrame({"category": categories, "value": [30, 25, 25, 20]})

    else:
        # Données par défaut
        data = pd.DataFrame({"x": range(10), "y": np.random.randint(1, 100, 10)})

    return data
