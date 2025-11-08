# What is this for?

This folder should be used to store configuration files used by Kedro or by separate tools.

This file can be used to provide users with instructions for how to reproduce local configuration with their own credentials. You can edit the file however you like, but you may wish to retain the information below and add your own section in the section titled **Instructions**.

## Local configuration

The `local` folder should be used for configuration that is either user-specific (e.g. IDE configuration) or protected (e.g. security keys).

> *Note:* Please do not check in any local configuration to version control.

## Base configuration

The `base` folder is for shared configuration, such as non-sensitive and project-related configuration that may be shared across team members.

WARNING: Please do not put access credentials in the base configuration folder.

## Find out more
You can find out more about configuration from the [user guide documentation](https://docs.kedro.org/en/stable/configuration/configuration_basics.html).

# Proyecto Analisis Kedro

Este proyecto tiene como objetivo analizar datos de ventas y compras de productos de mascotas, realizar un EDA (Exploratory Data Analysis) y preparar los datos para modelos de predicción y análisis de tendencias.

## Estructura del proyecto

- `data/` : Carpeta con datasets crudos, procesados y resultados intermedios.
- `src/analisis/` : Código fuente del proyecto.
  - `pipelines/data_ingestion/` : Ingesta de datos desde archivos.
  - `pipelines/data_processing/` : Transformaciones y unificación de datos.
  - `pipelines/data_analysis/` : Exploración y visualización de datos.
  - `pipelines/data_science/` : Modelos predictivos y análisis avanzados.
  - `nodes.py` : Funciones individuales para cada pipeline.

## Datos utilizados

- `matriz_de_datos_venta_normalizada.parquet`
- `matriz_de_datos_compra_normalizada.parquet`

Se unificaron en `matriz_de_datos_unificada_emparejada` con columna `TIPO` indicando si es venta o compra.

## Procesamiento de datos

- Se unificaron ventas y compras.
- Se ordenaron los datos por producto y fecha.
- Se agregaron columnas útiles como `AÑO_MES` para análisis temporal.

## Exploratory Data Analysis (EDA)

Se realizaron análisis como:

- Serie temporal de cantidad total por mes (ventas vs compras).
- Top 10 productos vendidos por mes y por comuna.
- Mapas de calor mostrando ventas por comuna y producto.
- Filtrado de outliers y enfoque en los productos más vendidos.

## Visualizaciones

- Gráficos de series temporales.
- Mapas de calor de ventas por comuna y producto.
- Histogramas y boxplots para detectar outliers.

## Próximos pasos

- Modelos predictivos: regresión lineal, árboles de decisión, etc.
- Análisis de tendencias y predicciones de demanda por producto y comuna.

## Cómo ejecutar el proyecto

1. Activar el entorno virtual:
   ```bash
   conda activate analisis
   2. Ejecutar el pipeline completo:
   ```bash
   kedro run
   
3. Para generar únicamente el EDA:
   ```bash
   kedro run --pipeline=data_analysis
   
Notas

Se recomienda revisar los parámetros en conf/base/parameters.yml para cambiar rutas o filtros.

El proyecto está preparado para agregar más pipelines de análisis y modelado predictivo.