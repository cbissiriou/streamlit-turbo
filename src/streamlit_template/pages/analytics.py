"""
Page Analytics - StreamlitTurbo PRO
Visualisations et analyse de données avec authentification requise
"""

from datetime import datetime

import streamlit as st

from streamlit_template.auth import require_auth
from streamlit_template.components import render_footer, render_header
from streamlit_template.components.charts import (
    create_bar_chart,
    create_line_chart,
    create_multi_line_chart,
    create_pie_chart,
    generate_sample_data,
)
from streamlit_template.monitoring import track_action, track_page_view

# Track page view
track_page_view("analytics")

# Header
render_header("📊 Analytics", "Visualisations et analyse de données")

# Authentification requise
@require_auth
def render_analytics_content():
    """Contenu de la page analytics (protégé)"""

    # Filtres en haut
    st.markdown("### 🔍 Filtres")
    col1, col2, col3 = st.columns(3)

    with col1:
        date_range = st.selectbox(
            "Période",
            ["7 jours", "30 jours", "90 jours", "1 an"],
            index=1,
        )

    with col2:
        category = st.multiselect(
            "Catégorie",
            ["Ventes", "Marketing", "Produit", "Support"],
            default=["Ventes", "Marketing"],
        )

    with col3:
        metric_type = st.selectbox(
            "Métrique",
            ["Utilisateurs", "Sessions", "Revenus", "Conversions"],
        )

    st.markdown("---")

    # KPIs principaux
    st.markdown("### 📈 KPIs Principaux")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Utilisateurs",
            value="12,543",
            delta="+15.3%",
        )

    with col2:
        st.metric(
            label="💰 Revenus",
            value="€45,231",
            delta="+8.7%",
        )

    with col3:
        st.metric(
            label="📊 Conversions",
            value="1,234",
            delta="-2.1%",
            delta_color="inverse",
        )

    with col4:
        st.metric(
            label="⏱️ Durée moy.",
            value="5m 32s",
            delta="+12s",
        )

    st.markdown("---")

    # Graphiques principaux
    st.markdown("### 📊 Visualisations")

    # Générer des données d'exemple
    data_line = generate_sample_data("line")
    data_bar = generate_sample_data("bar")
    data_pie = generate_sample_data("pie")

    # Onglets pour différentes vues
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendances", "📊 Comparaisons", "🥧 Répartition", "📋 Données"])

    with tab1:
        st.markdown("#### Évolution temporelle")
        fig_line = create_line_chart(
            data=data_line,
            x="date",
            y="value",
            title="Évolution des métriques",
            height=500,
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Graphique multi-lignes
        fig_multi = create_multi_line_chart(
            data=data_line,
            x="date",
            y_columns=["value", "value2"],
            title="Comparaison de métriques",
            height=400,
        )
        st.plotly_chart(fig_multi, use_container_width=True)

    with tab2:
        st.markdown("#### Analyse comparative")

        col1, col2 = st.columns(2)

        with col1:
            fig_bar = create_bar_chart(
                data=data_bar,
                x="category",
                y="value",
                title="Performance par catégorie",
                height=400,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Bar chart horizontal
            fig_bar_h = create_bar_chart(
                data=data_bar,
                x="category",
                y="value2",
                title="Métrique secondaire",
                orientation="v",
                height=400,
            )
            st.plotly_chart(fig_bar_h, use_container_width=True)

    with tab3:
        st.markdown("#### Répartition")

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = create_pie_chart(
                data=data_pie,
                values="value",
                names="category",
                title="Répartition par segment",
                height=400,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Donut chart
            fig_donut = create_pie_chart(
                data=data_pie,
                values="value",
                names="category",
                title="Distribution (Donut)",
                hole=0.4,
                height=400,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    with tab4:
        st.markdown("#### Données brutes")

        # Afficher les données
        st.dataframe(
            data_line,
            use_container_width=True,
            hide_index=False,
        )

        # Export
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Exporter CSV", use_container_width=True):
                csv = data_line.to_csv(index=False)
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f"analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                track_action("export_csv", page="analytics")

        with col2:
            if st.button("📥 Exporter JSON", use_container_width=True):
                json_data = data_line.to_json(orient="records", date_format="iso")
                st.download_button(
                    label="Télécharger JSON",
                    data=json_data,
                    file_name=f"analytics_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True,
                )
                track_action("export_json", page="analytics")

        with col3:
            if st.button("🔄 Rafraîchir données", use_container_width=True):
                st.cache_data.clear()
                st.rerun()

    st.markdown("---")

    # Insights automatiques
    with st.expander("🤖 Insights automatiques"):
        st.markdown("""
        **Tendances détectées:**
        - 📈 Croissance soutenue (+15.3%) sur les 30 derniers jours
        - 🎯 Meilleure performance le mardi et mercredi
        - 📊 Le segment "Marketing" représente 42% du total
        - ⚠️ Baisse de conversions à surveiller (-2.1%)

        **Recommandations:**
        - Augmenter les efforts marketing en début de semaine
        - Analyser les causes de la baisse de conversions
        - Capitaliser sur les segments performants
        """)


# Render le contenu avec protection auth
render_analytics_content()

# Footer
render_footer()
