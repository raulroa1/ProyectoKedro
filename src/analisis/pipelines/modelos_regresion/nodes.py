import warnings
import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV, KFold

# 🔹 Ignorar warnings innecesarios
warnings.filterwarnings("ignore")

# ==========================
# ===== Regresión ==========
# ==========================
def pre_proceso_rg(X, y, n_filas=56884):
    """
    🔹 Forzar tamaño fijo de n_filas en X e y
    🔹 Convierte y a 1D para evitar DataConversionWarning
    """
    y = y.iloc[:n_filas].reset_index(drop=True)
    X = X.iloc[:n_filas].reset_index(drop=True)
    print(f"✅ Tamaños forzados: X={len(X)}, y={len(y)}")
    return X, y

def dividir_datos_reg(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def entrenar_modelos_regresion_cv(X_train, y_train, output_path="models_reg"):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    modelos = {
        "LinearRegression": (LinearRegression(), {}),
        "Ridge": (Ridge(), {'alpha':[0.1,1.0,10.0]}),
        "Lasso": (Lasso(), {'alpha':[0.01,0.1,1.0]}),
        "RandomForest": (RandomForestRegressor(random_state=42, n_jobs=-1), {'n_estimators':[50,100]}),
        "GradientBoosting": (GradientBoostingRegressor(random_state=42), {'n_estimators':[50,100]}),
    }
    
    resultados_rg = {}
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    
    for nombre, (modelo, params) in modelos.items():
        if params:
            gs = GridSearchCV(modelo, params, cv=cv, n_jobs=-1)
            gs.fit(X_train, y_train)
            best_model = gs.best_estimator_
            best_params = gs.best_params_
            score_cv = gs.best_score_
        else:
            modelo.fit(X_train, y_train)
            best_model = modelo
            best_params = {}
            score_cv = None
        
        resultados_rg[nombre] = {
            "modelo": best_model,
            "mejor_params": best_params,
            "score_cv": score_cv
        }
        joblib.dump(best_model, f"{output_path}/{nombre}.pkl")
        print(f"✅ Modelo guardado: {nombre}")
    
    return resultados_rg

def evaluar_modelos_regresion(resultados, X_test, y_test):
    metricas = {}
    for nombre, res in resultados.items():
        y_pred = res['modelo'].predict(X_test)
        metricas[nombre] = {
            "RMSE": mean_squared_error(y_test, y_pred, squared=False),
            "MAE": mean_absolute_error(y_test, y_pred),
            "R2": r2_score(y_test, y_pred)
        }
    return pd.DataFrame(metricas).T
