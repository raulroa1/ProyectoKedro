from kedro.pipeline import Pipeline, node
from .nodes import mostrar_datos, add_weight_columns

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=mostrar_datos,
            inputs=["matriz_compra", "matriz_venta"],
            outputs=None,
            name="mostrar_datos_node",
        ),
        node(
            func=add_weight_columns,
            inputs="matriz_compra",
            outputs="df_compra_weighted",
            name="extract_weight_node",
        ),
        node(
            func=add_weight_columns,
            inputs="matriz_venta",
            outputs="df_venta_weighted",
            name="extract_weight_venta_node",
        ),
    ])
