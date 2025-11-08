"""Project pipelines."""

from typing import Dict

from kedro.pipeline import Pipeline

# Importa directamente los pipelines de tus módulos
from analisis.pipelines import data_processing as dp
from analisis.pipelines import data_analysis as da
from analisis.pipelines import data_ingestion as di
from analisis.pipelines import modelos_clasificacion as mc
from analisis.pipelines import modelos_regresion as mr
from analisis.pipelines import clustering as cl



def register_pipelines() -> dict[str, Pipeline]:
    return {
        "data_processing": dp.create_pipeline(),
        "data_analysis": da.create_pipeline(),
        "data_ingestion": di.create_pipeline(),
        "modelos_clasificacion": mc.create_pipeline(),
        "modelos_regresion": mr.create_pipeline(),
        "clustering": cl.create_pipeline(),
        "__default__": (
            dp.create_pipeline()
            + da.create_pipeline()
            + di.create_pipeline()
            + mc.create_pipeline()
            + mr.create_pipeline()
            + cl.create_pipeline()
        ),
    }
