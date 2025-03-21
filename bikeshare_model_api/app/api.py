"""API router module."""

import json
from typing import Any, Union

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger

from bikeshare_model import __version__ as model_version
from bikeshare_model.predict import make_prediction

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=schemas.HealthResponse, status_code=200)
def health() -> dict:
    """
    Root Get request to check health of the API.
    """
    health_data = schemas.Health(
        name=settings.PROJECT_NAME,
        api_version=__version__,
        model_version=model_version,
    )

    return {"status": "ok", "api_details": health_data}


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.BikeSharingDataInputSchema) -> Any:
    """
    Make bike sharing count predictions with the trained model.
    """
    # Convert input_data to a dictionary (not a DataFrame)
    input_dict = jsonable_encoder(input_data)
    
    logger.info(f"Making prediction with input: {input_dict}")
    
    try:
        # Pass the dictionary directly - your make_prediction function will convert it
        # to a DataFrame internally with pd.DataFrame([input_data])
        results = make_prediction(input_data=input_dict)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=results["errors"])

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results