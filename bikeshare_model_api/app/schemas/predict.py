"""Prediction schema."""

from typing import Optional, Union
import pandas as pd, datetime

from pydantic import BaseModel, Field


class BikeSharingDataInputSchema(BaseModel):
    """
    Input schema for bike sharing data prediction.
    
    These fields match the required inputs for your prediction model.
    """
    
    dteday: Optional[datetime.date]  = Field(..., description="Date (YYYY-MM-DD format)")
    season: Optional[str] = Field(..., description="Season (1:spring, 2:summer, 3:fall, 4:winter)")
    hr: Optional[str] = Field(..., description="Hour (0 to 23)")
    holiday: Optional[str] = Field(..., description="Holiday (0: No, 1: Yes)")
    weekday: Optional[str] = Field(..., description="Day of the week (0 to 6)")
    workingday: Optional[str] = Field(..., description="Working Day (0: No, 1: Yes)")
    weathersit: Optional[str] = Field(..., description="Weather (1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain)")
    temp: Optional[float] = Field(..., description="Temperature in Celsius")
    atemp: Optional[float] = Field(..., description="Feeling temperature in Celsius")
    hum: Optional[float] = Field(..., description="Humidity")
    windspeed: Optional[float] = Field(..., description="Wind speed")
    casual: Optional[int] = Field(None, description="Casual users count")
    registered: Optional[int] = Field(None, description="Registered users count")
    cnt: Optional[int] = Field(None, description="Total count")

    class Config:
        """Schema configuration."""
        
        # Updated for Pydantic v2 compatibility
        json_schema_extra = {
            "example": {
                "dteday": "2012-12-31",
                "season": 1,
                "hr": 14,
                "holiday": 0,
                "weekday": 1,
                "workingday": 1,
                "weathersit": 2,
                "temp": 0.32,
                "atemp": 0.36,
                "hum": 0.70,
                "windspeed": 0.34,
                "casual": None,
                "registered": None,
                "cnt": None
            }
        }


class PredictionResults(BaseModel):
    """Prediction results schema."""
    
    predictions: float
    version: str
    errors: Optional[str] = None