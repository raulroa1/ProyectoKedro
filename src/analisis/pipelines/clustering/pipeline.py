from kedro.pipeline import Pipeline, node
from .nodes import (
    escalar_datos,
    aplicar_pca,
    encontrar_k_optimo,
    entrenar_kmeans,
    evaluar_silhouette,
    graficar_clusters
)

def create_pipeline(**kwargs):
    return Pipeline([
        # 1. Escalado
        node(
            escalar_datos,
            inputs="X_procesada_rg",
            outputs="X_scaled",
            name="scaling"
        ),

        # 2. PCA Opcional
        node(
            aplicar_pca,
            inputs=["X_scaled", "params:pca_parameters"],
            outputs="X_pca",
            name="pca_transform"
        ),

        # 3. Método del Codo → Mejor K
        node(
            encontrar_k_optimo,
            inputs="X_pca",
            outputs="k_optimo",
            name="metodo_del_codo"
        ),

        # 4. Entrenamiento KMeans con K óptimo
        node(
            entrenar_kmeans,
            inputs=["X_pca", "k_optimo"],
            outputs="cluster_labels",
            name="train_kmeans"
        ),

        # 5. Evaluación con Silhouette Score
        node(
            evaluar_silhouette,
            inputs=["X_pca", "cluster_labels"],
            outputs="silhouette_score",
            name="cluster_silhouette_eval"
        ),
        node(
            graficar_clusters,
            inputs=["X_pca", "cluster_labels"],
            outputs="cluster_plot",
            name="plot_clusters"
        )
    ])
