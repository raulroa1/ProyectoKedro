from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

# Configuración del DAG
default_args = {
    'owner': 'raul',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Crear el DAG
dag = DAG(
    'kedro_ml_pipeline',
    default_args=default_args,
    description='Pipeline completo de Machine Learning con Kedro',
    schedule_interval=None,
    start_date=datetime(2025, 10, 1),
    catchup=False,
    max_active_runs=1,
    tags=['kedro', 'ml', 'analisis'],
)

# Tarea de inicio
start = DummyOperator(
    task_id='start_pipeline',
    dag=dag
)

# Pipeline de Ingestion de Datos
data_ingestion = BashOperator(
    task_id='run_data_ingestion',
    bash_command='cd /opt/airflow/analisis && python -m kedro run --pipeline=data_ingestion',
    dag=dag
)

# Pipeline de Procesamiento de Datos
data_processing = BashOperator(
    task_id='run_data_processing',
    bash_command='cd /opt/airflow/analisis && python -m kedro run --pipeline=data_processing',
    dag=dag
)

# Pipeline de Análisis Exploratorio
data_analysis = BashOperator(
    task_id='run_data_analysis',
    bash_command='cd /opt/airflow/analisis && python -m kedro run --pipeline=data_analysis',
    dag=dag
)

# Pipeline de Modelos de Clasificación
modelos_clasificacion = BashOperator(
    task_id='run_modelos_clasificacion',
    bash_command='cd /opt/airflow/analisis && python -m kedro run --pipeline=modelos_clasificacion',
    dag=dag
)

# Pipeline de Modelos de Regresión
modelos_regresion = BashOperator(
    task_id='run_modelos_regresion',
    bash_command='cd /opt/airflow/analisis && python -m kedro run --pipeline=modelos_regresion',
    dag=dag
)

# Tarea de finalización
end = DummyOperator(
    task_id='end_pipeline',
    dag=dag
)

# Definir dependencias
start >> data_ingestion
data_ingestion >> data_processing
data_processing >> data_analysis
data_analysis >> [modelos_clasificacion, modelos_regresion]
[modelos_clasificacion, modelos_regresion] >> end
