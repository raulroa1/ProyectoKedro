"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 1.0.0
"""
import pandas as pd

def categorize_weight_node(df: pd.DataFrame) -> pd.DataFrame:
    import re

    def categorize_weight(row):
        if re.search(r'\d+\s*\+\s*\d+[\,\.]*\d*\s*KG', row['PRODUCTO'], re.IGNORECASE):
            return "Bonus KG"
        elif row['Unit'] == 'KG':
            if row['Weight'] in [1.5, 2.5, 3, 4, 8, 9, 10, 15, 18, 19.5, 20, 25]:
                return f"{row['Weight']} KG"
            else:
                return "Other KG"
        elif row['Unit'] in ['GR', '12X100']:
            return "Pouch"
        elif row['Unit'] == 'CC':
            return "CC (ml/l)"
        elif row['Unit'] == 'UN':
            return "Units"
        else:
            return "Unknown"

    df['Weight_Category'] = df.apply(categorize_weight, axis=1)
    return df


def summarize_categories(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    Agrupa y resume categorías principales del dataset.
    Args:
        df: DataFrame de entrada con columnas categóricas.
    Returns:
        DataFrame con conteos por categoría.
    """
    summary = df['Weight_Category'].value_counts().reset_index()
    summary.columns = ['Category', 'Count']
    summary['Source'] = name
    return summary


