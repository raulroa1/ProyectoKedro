# pipeline_regresion.py
from kedro.pipeline import Pipeline, node
from .nodes import dividir_datos_reg, entrenar_modelos_regresion_cv, evaluar_modelos_regresion, pre_proceso_rg

def create_pipeline(**kwargs):
    return Pipeline(
        [    
            node(pre_proceso_rg,
                inputs=["X_procesada_rg","y_procesada_rg"],
                outputs=["preprocceso_reg_X","preprocceso_reg_y"],
                name="pre_proceso_rg_node"
            ),
            node(dividir_datos_reg,
                 inputs=["preprocceso_reg_X","preprocceso_reg_y"],
                 outputs=["X_train_reg","X_test_reg","y_train_reg","y_test_reg"],
                 name="dividir_datos_reg_node"),
            
            node(entrenar_modelos_regresion_cv,
                 inputs=["X_train_reg","y_train_reg"],
                 outputs="resultados_rg",
                 name="entrenar_modelos_regresion_node"),
            node(evaluar_modelos_regresion,
                 inputs=["resultados_rg", "X_test_reg", "y_test_reg"],
                 outputs="metricas_test",
                 name="evaluar_modelos_regresion_node"),
        ]
    )
