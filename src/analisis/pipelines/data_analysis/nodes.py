"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 1.0.0
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
def analizar_ventas_productos(matriz_venta_clean: pd.DataFrame, matriz_compra_clean: pd.DataFrame) -> None:
    """
    Análisis exploratorio de ventas y compras limpias.
    """
    print("=== 📦 MATRIZ VENTA CLEAN ===")
    print(matriz_venta_clean.head())
    print("\nEstadísticas de venta:")
    print(matriz_venta_clean.describe())

    print("\n=== 🛒 MATRIZ COMPRA CLEAN ===")
    print(matriz_compra_clean.head())
    print("\nEstadísticas de compra:")
    print(matriz_compra_clean.describe())

    # Top 10 productos más vendidos
    top_productos = (
        matriz_venta_clean["PRODUCTO_BASE"]
        .value_counts()
        .head(10)
        .index
    )
    
    df_top = matriz_venta_clean[matriz_venta_clean["PRODUCTO_BASE"].isin(top_productos)]

    plt.figure(figsize=(10, 6))
    
    sns.histplot(
        data=df_top,
        x="PRODUCTO_BASE",
        weights="CANTIDAD",
        bins=10,
        kde=False
    )

    plt.xticks(rotation=45, ha='right')
    plt.title("Distribución de ventas por producto base (Top 10)")
    plt.xlabel("Producto base")
    plt.ylabel("Cantidad total vendida")
    plt.tight_layout()
    plt.show()

# src/analisis/pipelines/data_analysis/nodes.py


def eda_unificado(df: pd.DataFrame, output_path: str) -> None:
    """
    Realiza un EDA básico del dataset unificado de ventas y compras.
    Guarda reportes y gráficas en la carpeta `output_path`.
    """
    os.makedirs(output_path, exist_ok=True)

    # 1. Información básica
    info_path = os.path.join(output_path, "info.txt")
    with open(info_path, "w") as f:
        f.write("=== INFO DEL DATASET ===\n")
        df.info(buf=f)
        f.write("\n\n=== DESCRIBE ===\n")
        f.write(df.describe(include='all').to_string())
        f.write("\n\n=== NULOS POR COLUMNA ===\n")
        f.write(df.isnull().sum().to_string())
    
    # 2. Distribuciones
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns
    for col in numeric_cols:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribución de {col}')
        plt.savefig(os.path.join(output_path, f'hist_{col}.png'))
        plt.close()

    # 3. Boxplots para outliers
    for col in numeric_cols:
        plt.figure(figsize=(6,4))
        sns.boxplot(x=df[col])
        plt.title(f'Boxplot de {col}')
        plt.savefig(os.path.join(output_path, f'box_{col}.png'))
        plt.close()

    # 4. Series temporales por mes
    if 'FECHA' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'])
        df['AÑO_MES'] = df['FECHA'].dt.to_period('M')
        pivot = df.groupby(['AÑO_MES','TIPO'])['CANTIDAD'].sum().unstack()
        pivot.plot(figsize=(10,5))
        plt.title("Cantidad total por mes (ventas vs compras)")
        plt.savefig(os.path.join(output_path, 'serie_temporal_cantidad.png'))
        plt.close()

    # 5. Productos top por cantidad
    top_productos = df.groupby('PRODUCTO_BASE')['CANTIDAD'].sum().sort_values(ascending=False).head(20)
    top_productos.plot(kind='bar', figsize=(12,5), title="Top 20 productos por cantidad")
    plt.ylabel("Cantidad total")
    plt.savefig(os.path.join(output_path, 'top_productos_cantidad.png'))
    plt.close()

