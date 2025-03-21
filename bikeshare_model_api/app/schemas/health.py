"""Health schemas."""

from pydantic import BaseModel

class Health(BaseModel):
    """Health model."""

    name: str
    api_version: str
    model_version: str


class HealthResponse(BaseModel):
    """Health response schema."""

    status: str
    api_details: Health