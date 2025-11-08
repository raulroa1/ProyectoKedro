# ProyectoKedro

Proyecto realizado con Kedro y la base de datos de Allendes.
Proyecto Análisis de Ventas

Este proyecto analiza datos de ventas y compras de productos, utilizando Kedro para la gestión de pipelines y Python para el análisis exploratorio y visualización.

Estructura del proyecto:
analisis/
│
├── conf/                  # Configuraciones (data paths, parámetros)
├── data/
│   ├── 01_raw/            # Datos crudos
│   ├── 02_intermediate/   # Datos procesados intermedios
│   └── 03_primary/        # Datos finales
├── src/analisis/
│   ├── pipelines/
│   │   ├── data_ingestion/   # Carga de datos
│   │   ├── data_processing/  # Limpieza y transformación
│   │   ├── data_analysis/    # EDA y visualizaciones
│   │   └── data_science/     # Modelos predictivos
│   └── utils/                # Funciones auxiliares
├── notebooks/               # Notebooks exploratorios
└── README.md

Flujo del Proyecto

Data Ingestion: Carga de datasets de ventas y compras.

Data Processing:

Unificación de ventas y compras en un solo dataframe.

Ordenamiento por fecha y producto.

Data Analysis (EDA):

Análisis descriptivo: conteo, estadísticas y nulos.

Series temporales: ventas por mes.

Top productos por mes y comuna.

Mapas de calor de ventas por comuna y producto (top 10).

Data Science:

Modelos de regresión, clasificación o árboles de decisión.

Predicción de ventas futuras.

Reporting:

Gráficos y resultados guardados en output_path.


Ejecución:

cd ProyectoKedroAllendes
cd analisis
instalar uvx en
crear el entorno virtual:
py -m venv .venv
Activar el entorno virtual:
conda activate analisis
# o
source .venv/Scripts/activate
# o
.venv/Scripts/activate
instalar dependencias
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

Ejecutar el pipeline completo:
kedro run

Para generar únicamente el EDA:
kedro run --pipeline=data_analysis
Los gráficos y reportes se guardarán en la carpeta definida en params:eda.output_path.

Dependencias
Python >= 3.10
pandas
numpy
matplotlib
seaborn
kedro

Instalación rápida:
pip install -r requirements.txt
Contacto
Cualquier duda o mejora, contactar a Raúl José Roa Astudillo 972968425, estudiante de Ingenieria en Informatica.











[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project with PySpark setup, which was generated using `kedro 1.0.0`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:


## How to run your Kedro pipeline

You can run your Kedro project with:


## How to test your Kedro project

Have a look at the files `tests/test_run.py` and `tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:


You can configure the coverage threshold in your project's `pyproject.toml` file under the `[tool.coverage.report]` section.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:


After installing Jupyter, you can start a local notebook server:


### JupyterLab
To use JupyterLab, you need to install it:


You can also start JupyterLab:


### IPython
And if you want to run an IPython session:


### IPython
And if you want to run an IPython session:


### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)
