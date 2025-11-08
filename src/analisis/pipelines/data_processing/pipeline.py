from kedro.pipeline import Pipeline, node
from .nodes import mostrar_datos, limpiar_caracteres_especiales, extraer_peso_y_limpiar_productos_v3, limpiar_productos, filtrar_por_peso, normalizar_productos, normalizar_datos, filtrar_8_meses_normalizados, preparar_datos_clasificacion, preparar_datos_regresion

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=mostrar_datos,
            inputs=["matriz_compra", "matriz_venta"],
            outputs=None,
            name="mostrar_datos_node",
        ),node(
            func=limpiar_caracteres_especiales,
            inputs="matriz_compra",
            outputs="matriz_compra_clean_caracteres",
            name="limpiar_compra_caracteres",
        ),
        node(
            func=limpiar_caracteres_especiales,
            inputs="matriz_venta",
            outputs="matriz_venta_clean_caracteres",
            name="limpiar_venta_caracteres",
        ),        
        node(
            func=limpiar_productos,
            inputs="matriz_compra_clean_caracteres",
            outputs="matriz_compra_limpia",
            name="limpiar_compra_node",
        ),
        node(
            func=limpiar_productos,
            inputs="matriz_venta_clean_caracteres",
            outputs="matriz_venta_limpia",
            name="limpiar_venta_node",
        ),
        node(
            func=extraer_peso_y_limpiar_productos_v3,
            inputs="matriz_venta_limpia",         # dataset original en catalog.yml
            outputs="matriz_venta_clean",  # dataset limpio con columnas nuevas
            name="extraer_peso_y_limpiar_productos_venta_node"
        ),
        node(
            func=extraer_peso_y_limpiar_productos_v3,
            inputs="matriz_compra_limpia",         # dataset original en catalog.yml
            outputs="matriz_compra_clean",  # dataset limpio con columnas nuevas
            name="extraer_peso_y_limpiar_productos_compra_node"
        ),
        node(
            filtrar_por_peso,
            inputs=[
                "matriz_venta_clean",
                "params:filtrado_peso.ventas.min",
                "params:filtrado_peso.ventas.max"
            ],
            outputs="matriz_venta_filtrada",
            name="filtrar_ventas_node"
        ),
        # Nodo para compras
        node(
            filtrar_por_peso,
            inputs=[
                "matriz_compra_clean",
                "params:filtrado_peso.compras.min",
                "params:filtrado_peso.compras.max"
            ],
            outputs="matriz_compra_filtrada",
            name="filtrar_compras_node"
        ),
        node(
            func=normalizar_productos,
            inputs="matriz_venta_filtrada",  # o "matriz_compra_filtrada"
            outputs="matriz_venta_normalizada",  # o "matriz_compra_normalizada"
            name="normalizar_productos_ventas_node"
        ),
        node(
            func=normalizar_productos,
            inputs="matriz_compra_filtrada",
            outputs="matriz_compra_normalizada",
            name="normalizar_productos_compras_node"
        ),
        node(
            func=normalizar_datos,
            inputs="matriz_venta_filtrada",
            outputs="matriz_venta_datos_normalizada",
            name="normalizar_venta_node"
        ),
        node(
            func=normalizar_datos,
            inputs="matriz_compra_filtrada",
            outputs="matriz_compra_datos_normalizada",
            name="normalizar_compra_node"
        ),
        node(
            func=filtrar_8_meses_normalizados,
            inputs=["matriz_venta_datos_normalizada", "matriz_compra_datos_normalizada"],
            outputs=["df_venta_8meses", "df_compra_8meses", "meses_comunes_8"],
            name="filtrar_8_meses_normalizados_node"
        ),
        node(
            func=preparar_datos_clasificacion,
            inputs="df_venta_8meses",
            outputs=["procesamiento_X", "procesamiento_y"],
            name="preparar_datos_clasificacion_node"
        ),
        node(func=preparar_datos_regresion,
            inputs="df_venta_8meses",
            outputs=["X_procesada_rg","y_procesada_rg"],
            name="preparar_datos_regresion"
        ),
    ])
