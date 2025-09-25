"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Pipeline, node
from .nodes import mostrar_datos

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=mostrar_datos,
            inputs="matriz_compra",
            outputs=None,
            name="mostrar_datos_compra",
        ),
        node(
            func=mostrar_datos,
            inputs="matriz_venta",
            outputs=None,
            name="mostrar_datos_venta",
        ),
    ])
