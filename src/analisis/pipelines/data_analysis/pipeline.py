"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Pipeline, node
from .nodes import summarize_categories, categorize_weight_node

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=categorize_weight_node,
            inputs="df_compra_weighted",
            outputs="df_compra_categorized",
            name="categorize_weight_compra_node",
        ),
        node(
            func=categorize_weight_node,
            inputs="df_venta_weighted",
            outputs="df_venta_categorized",
            name="categorize_weight_venta_node",
        ),
        node(
            func=summarize_categories,
            inputs=dict(df="df_compra_weighted", name="params:compra_name"),
            outputs="compra_summary",
            name="summarize_compra",
        ),
        node(
            func=summarize_categories,
            inputs=dict(df="df_venta_weighted", name="params:venta_name"),
            outputs="venta_summary",
            name="summarize_venta",
        ),
    ])
