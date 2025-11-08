import pandas as pd
import re
from typing import Tuple, List
from sklearn.preprocessing import LabelEncoder

def mostrar_datos(matriz_compra: pd.DataFrame, matriz_venta: pd.DataFrame) -> None:
    print("=== MATRIZ COMPRA ===")
    print(matriz_compra.head())
    print("\n=== MATRIZ VENTA ===")
    print(matriz_venta.head())


def limpiar_caracteres_especiales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaza caracteres problemáticos (como comillas ‘ ’) por simples o los elimina.
    """
    def clean_text(s):
        if isinstance(s, str):
            # Reemplaza comillas inteligentes y otros caracteres no ASCII
            s = s.replace('\x91', "'").replace('\x92', "'")
            s = s.replace('\x93', '"').replace('\x94', '"')
            # Elimina otros caracteres no imprimibles
            s = re.sub(r'[^\x20-\x7EÁÉÍÓÚÑáéíóúñ]', '', s)
            return s.strip()
        return s

    return df.applymap(clean_text)

def limpiar_productos(df: pd.DataFrame) -> pd.DataFrame:
    df["PRODUCTO"] = df["PRODUCTO"].str.strip().str.upper()
    df["TIP_DOC"] = df["TIP_DOC"].str.strip()
    df["COMUNA"] = df["COMUNA"].str.strip()
    # Limpiar caracteres especiales
    df = limpiar_caracteres_especiales(df)
    return df

def extraer_peso_y_limpiar_productos_v3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia los nombres de productos, extrae el peso en KG y crea un nombre base,
    además de limpiar caracteres especiales.
    """
    def extraer_peso(nombre: str) -> float:
        nombre = nombre.upper()
        match_kg = re.search(r'(\d+[.,]?\d*)\s*KG', nombre)
        if match_kg:
            return float(match_kg.group(1).replace(',', '.'))
        match_gr = re.search(r'(\d+[.,]?\d*)\s*GR', nombre)
        if match_gr:
            return float(match_gr.group(1).replace(',', '.')) / 1000
        match_mult = re.search(r'(\d+)\s*X\s*(\d+)', nombre)
        if match_mult:
            return float(match_mult.group(1)) * float(match_mult.group(2)) / 1000
        return None

    df["PRODUCTO"] = df["PRODUCTO"].str.strip().str.upper()
    df["PESO_KG"] = df["PRODUCTO"].apply(extraer_peso)
    df["PRODUCTO_BASE"] = df["PRODUCTO"]\
        .str.replace(r'X\s*\d+(\s*(KG|GR))?', '', regex=True)\
        .str.replace(r'\d+\s*X\s*\d+', '', regex=True)\
        .str.replace(r'\d+[.,]?\d*KG', '', regex=True)\
        .str.replace(r'\d+', '', regex=True)\
        .str.strip()

    # Limpiar caracteres especiales en todo el dataframe antes de guardar
    df = limpiar_caracteres_especiales(df)
    return df


def ordenar_por_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena los datos por tipo de documento y fecha de forma ascendente.
    """
    df_ordenado = df.sort_values(by=['TIP_DOC', 'FECHA']).reset_index(drop=True)
    return df_ordenado



def unificar_ventas_compras(venta_df: pd.DataFrame, compra_df: pd.DataFrame) -> pd.DataFrame:
    # Agregar columna para diferenciar tipo
    venta_df = venta_df.copy()
    compra_df = compra_df.copy()
    
    venta_df['TIPO'] = 'VENTA'
    compra_df['TIPO'] = 'COMPRA'
    
    # Unificar
    df_unificado = pd.concat([venta_df, compra_df], ignore_index=True)
    
    # Opcional: ordenar por fecha y producto
    df_unificado = df_unificado.sort_values(['PRODUCTO_BASE', 'FECHA']).reset_index(drop=True)
    
    return df_unificado

def filtrar_por_peso(df: pd.DataFrame, peso_min: float, peso_max: float) -> pd.DataFrame:
    return df[(df['PESO_KG'] >= peso_min) & (df['PESO_KG'] <= peso_max)]

def normalizar_productos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega una columna PRODUCTO_BASE_NORMAL al dataframe, normalizando el nombre del producto.
    """
    def normalizar(nombre):
        nombre = nombre.lower()                      # pasar a minúsculas
        nombre = re.sub(r'\d+(\.\d+)?', '', nombre) # quitar números
        nombre = re.sub(r'[^\w\s]', '', nombre)     # quitar signos de puntuación
        nombre = re.sub(r'\s+', ' ', nombre)        # espacios extra
        return nombre.strip()                        # quitar espacios al inicio y fin

    df['PRODUCTO_BASE_NORMAL'] = df['PRODUCTO_BASE'].apply(normalizar)
    return df

def normalizar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas, tipos de datos y formatos para un DataFrame de ventas o compras."""
    
    # Asegurar mayúsculas en los nombres de columnas
    df.columns = [col.strip().upper() for col in df.columns]

    # Limpiar espacios en texto
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # Convertir tipos
    df["CANTIDAD"] = pd.to_numeric(df["CANTIDAD"], errors="coerce")
    df["PESO_KG"] = pd.to_numeric(df["PESO_KG"], errors="coerce")
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    # Eliminar nulos críticos
    df = df.dropna(subset=["FECHA", "CANTIDAD", "PESO_KG"])

    # Resetear índice
    df = df.reset_index(drop=True)

    return df


def filtrar_8_meses_normalizados(df_venta: pd.DataFrame, df_compra: pd.DataFrame, year: int = 2025, meses_max: int = 8):
    # Asegurar formato datetime
    df_venta['FECHA'] = pd.to_datetime(df_venta['FECHA'], errors='coerce')
    df_compra['FECHA'] = pd.to_datetime(df_compra['FECHA'], errors='coerce')

    # Filtrar por año
    df_venta_ano = df_venta[df_venta['FECHA'].dt.year == year].copy()
    df_compra_ano = df_compra[df_compra['FECHA'].dt.year == year].copy()

    # Meses únicos
    meses_venta = sorted(df_venta_ano['FECHA'].dt.month.unique())
    meses_compra = sorted(df_compra_ano['FECHA'].dt.month.unique())

    # Meses comunes limitados a meses_max
    meses_comunes = sorted(list(set(meses_venta).intersection(meses_compra)))[:meses_max]

    # Filtrar los dataframes solo a esos meses
    df_venta_filtrado = df_venta_ano[df_venta_ano['FECHA'].dt.month.isin(meses_comunes)]
    df_compra_filtrado = df_compra_ano[df_compra_ano['FECHA'].dt.month.isin(meses_comunes)]

    # Convertir lista de meses a DataFrame
    df_meses_comunes = pd.DataFrame({'MES': meses_comunes})

    return df_venta_filtrado, df_compra_filtrado, df_meses_comunes



def preprocesar_ventas(df):
    df = df.copy()
    
    # --- Features básicas ---
    df['MES'] = df['FECHA'].dt.month
    df['PRODUCTO_ID'] = df['PRODUCTO'].astype('category').cat.codes
    df['COMUNA_ID'] = df['COMUNA'].astype('category').cat.codes
    
    # --- Filtrado por percentiles para eliminar outliers ---
    q_low = df['CANTIDAD'].quantile(0.01)   # 1er percentil
    q_high = df['CANTIDAD'].quantile(0.99)  # 99º percentil
    df = df[(df['CANTIDAD'] >= q_low) & (df['CANTIDAD'] <= q_high)]
    
    # --- Ordenar para calcular ventas anteriores ---
    df = df.sort_values(['PRODUCTO_ID','COMUNA_ID','FECHA'])
    
    # --- Feature histórica para clasificación binaria ---
    df['VENTA_MES_ANTERIOR'] = df.groupby(['PRODUCTO_ID','COMUNA_ID'])['CANTIDAD'].shift(1)
    df = df.dropna(subset=['VENTA_MES_ANTERIOR'])
    df['AUMENTA'] = (df['CANTIDAD'] > df['VENTA_MES_ANTERIOR']).astype(int)
    
    # --- Clasificación multiclase usando terciles ---
    df['VENTA_CLASE'] = pd.qcut(df['CANTIDAD'], q=3, labels=['baja','media','alta'], duplicates='drop')
    
    # --- Selección final de columnas ---
    columnas_finales = [
        'FECHA','PRODUCTO','COMUNA','CANTIDAD','MES','PRODUCTO_ID','COMUNA_ID',
        'VENTA_MES_ANTERIOR','AUMENTA','VENTA_CLASE'
    ]
    
    df = df[columnas_finales]
    
    return df


import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preparar_datos_clasificacion(df: pd.DataFrame):
    """
    Prepara los datos para clasificación:
      - Limpia fechas inválidas
      - Genera variables temporales y agrupadas
      - Calcula indicadores de ventas
      - Clasifica niveles de venta
      - Convierte variables a entero
      - Retorna X (features) e y (target)
    """

    df = df.copy()
    print("🔹 Iniciando preparación de datos para clasificación...")

    # ======================
    # 🔹 LIMPIEZA BÁSICA
    # ======================
    df.columns = df.columns.str.strip()  # eliminar espacios en nombres
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df = df.dropna(subset=["FECHA"])
    print(f"✅ Fechas válidas: {df.shape[0]} filas restantes")

    # ======================
    # 🔹 VARIABLES BASE
    # ======================
    df["MES"] = df["FECHA"].dt.month
    df["PRODUCTO_ID"] = df["PRODUCTO"].astype("category").cat.codes
    df["COMUNA_ID"] = df["COMUNA"].astype("category").cat.codes

    # ======================
    # 🔹 VARIABLES AGRUPADAS
    # ======================
    grp = df.groupby(["PRODUCTO_ID", "COMUNA_ID"])["CANTIDAD"]
    df["VENTA_MES_ANTERIOR"] = grp.shift(1)
    df["PROM_3_MESES"] = grp.shift(1).rolling(3, min_periods=1).mean()
    df["PROM_6_MESES"] = grp.shift(1).rolling(6, min_periods=1).mean()
    df["DELTA_MES"] = (df["CANTIDAD"] - df["VENTA_MES_ANTERIOR"]) / df["VENTA_MES_ANTERIOR"]

    # ======================
    # 🔹 CLASIFICACIÓN DE VENTAS
    # ======================
    bins = [0, 10, 50, df["CANTIDAD"].max()]
    labels = [0, 1, 2]
    df["VENTA_CLASE"] = pd.cut(df["CANTIDAD"], bins=bins, labels=labels)

    # ======================
    # 🔹 LIMPIEZA FINAL DE NULOS
    # ======================
    antes = len(df)
    df = df.dropna(subset=["VENTA_MES_ANTERIOR", "VENTA_CLASE"])
    despues = len(df)
    print(f"🧹 Filas eliminadas por nulos: {antes - despues}")
    print(f"📏 Tamaño después de limpieza: {df.shape}")

    # ======================
    # 🔹 CONVERSIÓN A ENTERO
    # ======================
    columnas_a_convertir = [
        "MES", "PRODUCTO_ID", "COMUNA_ID",
        "VENTA_MES_ANTERIOR", "PROM_3_MESES",
        "PROM_6_MESES", "DELTA_MES"
    ]

    # Validar existencia
    faltantes = [c for c in columnas_a_convertir if c not in df.columns]
    if faltantes:
        raise ValueError(f"❌ Faltan columnas en el dataset: {faltantes}")

    # Rellenar y convertir
    df[columnas_a_convertir] = df[columnas_a_convertir].fillna(0)
    df[columnas_a_convertir] = df[columnas_a_convertir].apply(lambda x: x.round().astype(int))

    # ======================
    # 🔹 VARIABLES X E Y
    # ======================
    X = df[columnas_a_convertir].reset_index(drop=True)
    y = pd.DataFrame(LabelEncoder().fit_transform(df["VENTA_CLASE"]), columns=["VENTA_CLASE"]).reset_index(drop=True)

    # ======================
    # 🔹 INFO FINAL
    # ======================
    print("\n✅ Columnas convertidas a entero:")
    print(df[columnas_a_convertir].dtypes)
    print("\n📊 Resumen final:")
    print(f"➡️  Filas totales: {df.shape[0]}")
    print(f"➡️  Columnas totales: {df.shape[1]}")
    print(f"➡️  X shape: {X.shape}, y shape: {y.shape}")
    print(f"➡️  Nulos restantes:\n{df.isna().sum()}")

    return X, y

def preparar_datos_regresion(df: pd.DataFrame):
    df = df.copy()
    # ======================
    # 🔹 LIMPIEZA BÁSICA
    # ======================
    df.columns = df.columns.str.strip()  # eliminar espacios en nombres
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df = df.dropna(subset=["FECHA"])
    print(f"✅ Fechas válidas: {df.shape[0]} filas restantes")
    # ======================
    # 🔹 VARIABLES BASE
    # ======================
    df["MES"] = df["FECHA"].dt.month
    df["PRODUCTO_ID"] = df["PRODUCTO"].astype("category").cat.codes
    df["COMUNA_ID"] = df["COMUNA"].astype("category").cat.codes
    df['MES'] = df['FECHA'].dt.month
    df['PRODUCTO_ID'] = df['PRODUCTO'].astype('category').cat.codes
    df['COMUNA_ID'] = df['COMUNA'].astype('category').cat.codes

    df.sort_values(['PRODUCTO_ID','COMUNA_ID','MES'], inplace=True)
    grp = df.groupby(['PRODUCTO_ID','COMUNA_ID'])['CANTIDAD']
    df['VENTA_MES_ANTERIOR'] = grp.shift(1)
    df['PROM_3_MESES'] = grp.shift(1).rolling(3,min_periods=1).mean()
    df['PROM_6_MESES'] = grp.shift(1).rolling(6,min_periods=1).mean()
    df['DELTA_MES'] = (df['CANTIDAD'] - df['VENTA_MES_ANTERIOR']) / df['VENTA_MES_ANTERIOR']

    df = df.dropna(subset=['VENTA_MES_ANTERIOR'])
    X = df[['MES','PRODUCTO_ID','COMUNA_ID','VENTA_MES_ANTERIOR','PROM_3_MESES','PROM_6_MESES','DELTA_MES']]
    y = df['CANTIDAD']

    # ======================
    # 🔹 INFO FINAL
    # ======================
    print("\n✅ Columnas convertidas a entero:")
    print(df.dtypes)
    print("\n📊 Resumen final:")
    print(f"➡️  Filas totales: {df.shape[0]}")
    print(f"➡️  Columnas totales: {df.shape[1]}")
    print(f"➡️  X shape: {X.shape}, y shape: {y.shape}")
    print(f"➡️  Nulos restantes:\n{df.isna().sum()}")

    return X, y
