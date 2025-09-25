import pandas as pd

def mostrar_datos(df: pd.DataFrame) -> None:
    """Muestra información básica del dataset."""
    print("Primeras filas:")
    print(df.head())
    print("\nResumen:")
    print(df.describe())
