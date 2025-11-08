"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import analizar_ventas_productos, eda_unificado

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=analizar_ventas_productos,
            inputs=["matriz_compra_datos_normalizada", "matriz_venta_datos_normalizada"],
            outputs=None,
            name="analizar_ventas_productos_node"
        ),
    ])

