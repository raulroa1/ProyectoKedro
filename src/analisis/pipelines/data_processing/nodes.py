import pandas as pd
import re

def mostrar_datos(matriz_compra: pd.DataFrame, matriz_venta: pd.DataFrame) -> None:
    print("=== MATRIZ COMPRA ===")
    print(matriz_compra.head())
    print("\n=== MATRIZ VENTA ===")
    print(matriz_venta.head())

def extract_weight(product_name):
    """
    Extracts the weight and unit (KG or GR) from a product name.
    Returns a tuple of (weight, unit) or (None, None) if no weight is found.
    """
    weight_match = re.search(r'(\d+)\s*(KG|GR)', product_name, re.IGNORECASE)
    if weight_match:
        weight = int(weight_match.group(1))
        unit = weight_match.group(2).upper()
        return weight, unit
    return None, None

def add_weight_columns(matriz_compra: pd.DataFrame) -> pd.DataFrame:
    matriz_compra = matriz_compra.copy()
    matriz_compra[['Weight', 'Unit']] = matriz_compra['PRODUCTO'].apply(lambda x: pd.Series(extract_weight(x)))
    
    # Crear categorías de peso (ajusta los rangos según tu necesidad)
    def categorize_weight(row):
        if row['Weight'] < 100:
            return 'Light'
        elif row['Weight'] < 500:
            return 'Medium'
        else:
            return 'Heavy'
    
    matriz_compra['Weight_Category'] = matriz_compra.apply(categorize_weight, axis=1)
    
    return matriz_compra

    
