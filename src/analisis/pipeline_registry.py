"""Project pipelines."""

from typing import Dict

from kedro.pipeline import Pipeline
from analisis.pipelines import data_processing
from kedro.framework.project import pipelines
from analisis.pipelines.data_ingestion.pipeline import create_pipeline as ingestion_pipeline
from analisis.pipelines.data_processing.pipeline import create_pipeline as processing_pipeline
from analisis.pipelines.data_analysis.pipeline import create_pipeline as analysis_pipeline

def register_pipelines() -> dict:
    return {
        "ingestion": ingestion_pipeline(),
        "processing": processing_pipeline(),
        "analysis": analysis_pipeline(),
        "__default__": ingestion_pipeline() + processing_pipeline() + analysis_pipeline(),
    }
