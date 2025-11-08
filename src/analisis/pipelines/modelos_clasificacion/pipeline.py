from kedro.pipeline import Pipeline, node
from .nodes import (
    dividir_datos_clf,
    entrenar_modelos_clasificacion_cv,
    evaluar_modelos_clasificacion,
    pre_proceso_clf
)

def create_pipeline(**kwargs):
    return Pipeline([     
      # 1. Dividir datos
      node(pre_proceso_clf,
         inputs=["X_procesada_clf","y_procesada_clf"],
         outputs=["preprocceso_x","preprocceso_y"],
         name="pre_proceso_clf_node"
      ),
      node(dividir_datos_clf,
         inputs=["preprocceso_x","preprocceso_y"],
         outputs=["X_train_clf","X_test_clf","y_train_clf","y_test_clf"],
         name="dividir_datos_clf_node"
      ),# 2. Entrenar modelos
      node(entrenar_modelos_clasificacion_cv,
         inputs=["X_train_clf","y_train_clf"],
         outputs="resultados_clf",
         name="entrenar_modelos_clasificacion_node"
      ),# 3. Evaluar métricas en test
      node(evaluar_modelos_clasificacion,
         inputs=["resultados_clf","X_test_clf","y_test_clf"],
         outputs="metricas_test_clf",
         name="evaluar_modelos_clasificacion_test_node"
      ),
    ])

