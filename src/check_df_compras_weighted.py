import pandas as pd
import os

# Ruta del CSV que debería haberse generado
csv_path = "data/02_intermediate/compras_weighted.csv"

# 1️⃣ Verificar que el archivo exista
if not os.path.exists(csv_path):
    print(f"❌ El archivo no se encontró en {csv_path}")
else:
    print(f"✅ El archivo existe: {csv_path}")
    
    # 2️⃣ Leer el CSV
    df = pd.read_csv(csv_path)
    
    # 3️⃣ Verificar que tenga las columnas Weight y Unit
    required_columns = ["Weight", "Unit"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Faltan columnas: {missing_columns}")
    else:
        print(f"✅ Todas las columnas están presentes: {required_columns}")
        print("Primeras filas del DataFrame:")
        print(df.head())
