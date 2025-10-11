import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def mostrar_datos(df: pd.DataFrame) -> dict:
    """Retorna información descriptiva del dataset en formato estructurado."""
    resumen = {
        "primeras_filas": df.head().to_dict(),
        "resumen_estadistico": df.describe().to_dict(),
        "num_filas": len(df),
        "columnas": list(df.columns),
    }
    return resumen


def factorizacion_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if 'COMUNA' in df.columns:
        df['COMUNA_ID'] = pd.factorize(df['COMUNA'])[0]
        print("\nPrimeras filas con COMUNA_ID:")
        print(df[['COMUNA', 'COMUNA_ID']].head())

        print("\nÚltimas filas con COMUNA_ID:")
        print(df[['COMUNA', 'COMUNA_ID']].tail())
    else:
        print("\n La columna 'COMUNA' no se encuentra en el DataFrame.")



def graficos_dataframe(df: pd.DataFrame, columna: str = 'CANTIDAD', bins: int = 10) -> Figure:
    """
    Genera un histograma de una columna específica del DataFrame.

    Args:
        df (pd.DataFrame): Dataset que contiene los datos.
        columna (str): Nombre de la columna a graficar (por defecto 'CANTIDAD').
        bins (int): Número de intervalos del histograma.

    Returns:
        matplotlib.figure.Figure: Figura del histograma generada.
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")

    # Crear figura y eje
    fig, ax = plt.subplots()

    # Generar histograma
    ax.hist(df[columna].dropna(), bins=bins, edgecolor='black')
    ax.set_xlabel(columna)
    ax.set_ylabel('Frecuencia')
    ax.set_title(f'Histograma de {columna}')
    ax.grid(True, alpha=0.3)

    # Retornar figura sin mostrarla
    return fig
