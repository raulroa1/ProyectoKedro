"""
This is a boilerplate pipeline 'modelos_clasificacion'
generated using Kedro 1.0.0
"""
import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# ==========================
# ===== Clasificación ======
# ==========================
def pre_proceso_clf(X,y):
# 🔹 Forzar tamaño fijo de 56884 filas en X e y
    y = y.iloc[:56884].reset_index(drop=True)
    X = X.iloc[:56884].reset_index(drop=True)
    # 🔹 Forzar tamaño fijo de 56884 filas en X e y
    print(f"✅ Tamaños forzados: X={len(X)}, y={len(y)}")
    print(type(X))
    print(type(y))
    return X,y

def dividir_datos_clf(X, y):
    print("📦 Entradas dividir_datos_clf:", len(X), len(y))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("✅ Salidas dividir_datos_clf:", len(X_train), len(y_train))
    return X_train, X_test, y_train, y_test

# ==========================
# === Entrenamiento modelos ==
# ==========================
def entrenar_modelos_clasificacion_cv(X_train_clf, y_train_clf, output_path="models_clf"):
    # 🔹 Aseguramos consistencia
    modelos = {
        "LogisticRegression": (LogisticRegression(max_iter=1000), {'C':[0.01,0.1,1,10]}),
        "RandomForest": (RandomForestClassifier(random_state=42), {'n_estimators':[50,100,200]}),
        "GradientBoosting": (GradientBoostingClassifier(random_state=42), {'n_estimators':[50,100]}),
        "SVC": (SVC(probability=True), {'C':[0.1,1,10]}),
        "KNN": (KNeighborsClassifier(), {'n_neighbors':[3,5,7]})
    }
    
    resultados_clf = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for nombre, (modelo, params) in modelos.items():
        print(f"\nEntrenando {nombre}...")
        gs = GridSearchCV(modelo, params, cv=cv, n_jobs=-1)
        gs.fit(X_train_clf, y_train_clf)
        resultados_clf[nombre] = {
            "modelo": gs.best_estimator_,
            "mejor_params": gs.best_params_,
            "score_cv": gs.best_score_
        }
        joblib.dump(gs.best_estimator_, f"{output_path}/{nombre}.pkl")
    
    return resultados_clf


# ==========================
# === Evaluación modelos ===
# ==========================
def evaluar_modelos_clasificacion(resultados, X_test, y_test):
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    metricas = {}
    for nombre, res in resultados.items():
        y_pred = res['modelo'].predict(X_test)
        metricas[nombre] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
            "Recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
            "F1": f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
    return pd.DataFrame(metricas).T
