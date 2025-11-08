import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def escalar_datos(data):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)
    return scaled


def aplicar_pca(data, pca_parameters):
    n = pca_parameters["n_components"]
    pca = PCA(n_components=n)
    data_pca = pca.fit_transform(data)
    return data_pca


def encontrar_k_optimo(data):
    distortions = []
    K = range(2, 11)

    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
        distortions.append(kmeans.inertia_)

    # Escoge el k con mayor cambio relativo (codo simple)
    dif = [abs(distortions[i] - distortions[i-1]) for i in range(1, len(distortions))]
    k_opt = dif.index(max(dif)) + 2  # +2 para alinearlo con rango inicial (2-11)

    print(f"✅ K óptimo encontrado: {k_opt}")
    return k_opt


def entrenar_kmeans(data, k):
    modelo = KMeans(n_clusters=k, random_state=42)
    labels = modelo.fit_predict(data)
    return labels


def evaluar_silhouette(data, labels):
    score = silhouette_score(data, labels)
    print(f"🔹 Silhouette Score: {score:.4f}")
    return score


def graficar_clusters(data_pca, labels):
    fig, ax = plt.subplots(figsize=(8,6))
    scatter = ax.scatter(data_pca[:,0], data_pca[:,1], c=labels, s=15)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("Clusters visualizados en espacio PCA")
    fig.colorbar(scatter, label="Cluster")

    return fig  # 👈 Importante: retornamos FIGURA
