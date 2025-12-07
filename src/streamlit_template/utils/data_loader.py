"""
Utilitaires pour charger les données
"""

from pathlib import Path

import pandas as pd


def load_sample_data() -> pd.DataFrame:
    """Charge le dataset d'exemple depuis le fichier CSV"""
    data_path = Path(__file__).parent.parent.parent.parent / "data" / "sample_data.csv"

    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        # Données de fallback si le fichier n'existe pas
        return pd.DataFrame(
            {
                "date": ["2024-01-15", "2024-01-16", "2024-01-17"],
                "product": ["Product A", "Product B", "Product C"],
                "sales": [1200, 800, 950],
                "quantity": [24, 16, 19],
                "region": ["Nord", "Sud", "Est"],
            }
        )


def get_data_summary(df: pd.DataFrame) -> dict:
    """Retourne un résumé des données"""
    return {
        "total_rows": len(df),
        "total_sales": df["sales"].sum() if "sales" in df.columns else 0,
        "unique_products": df["product"].nunique() if "product" in df.columns else 0,
        "date_range": f"{df['date'].min()} - {df['date'].max()}" if "date" in df.columns else "N/A",
    }
