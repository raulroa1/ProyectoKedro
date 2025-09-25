import re
import pandas as pd

def extract_weight(product_name: str):
    """
    Extrae el peso y la unidad (KG o GR) de un nombre de producto.
    Retorna una tupla (weight, unit) o (None, None) si no encuentra peso.
    """
    weight_match = re.search(r'(\d+)\s*(KG|GR)', product_name, re.IGNORECASE)
    if weight_match:
        weight = int(weight_match.group(1))
        unit = weight_match.group(2).upper()
        return weight, unit
    return None, None


def add_weight_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Node para agregar columnas 'Weight' y 'Unit' al DataFrame.
    """
    df[['Weight', 'Unit']] = df['PRODUCTO'].apply(lambda x: pd.Series(extract_weight(x)))
    return df
