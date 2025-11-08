"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 1.0.0
"""
from kedro.pipeline import Pipeline, node
from .nodes import mostrar_datos, graficos_dataframe



def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=mostrar_datos,
            inputs="matriz_compra_datos_normalizada",
            outputs="output_mostrar_datos_compra",
            name="mostrar_datos_compra",
        ),
        node(
            func=mostrar_datos,
            inputs="matriz_venta_datos_normalizada",
            outputs="output_mostrar_datos_venta",
            name="mostrar_datos_venta",
        ),
        node(
            func=graficos_dataframe,
            inputs="matriz_compra_datos_normalizada",
            outputs="output_mostrar_graficos_compra",
            name="graficos_dataframe_compra",
        ),
        node(
            func=graficos_dataframe,
            inputs="matriz_venta_datos_normalizada",
            outputs="output_mostrar_graficos_venta",
            name="graficos_dataframe_venta",
        ),
    ])
