"""Main FastAPI app instance."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging

# Setup logging first, before importing any module that might use logging
setup_app_logging(config=settings)


def get_application() -> FastAPI:
    """
    Initialize FastAPI application.
    
    Returns:
        FastAPI: FastAPI application instance
    """
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set up CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = get_application()


@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    """
    logger.info("Starting up Bike Sharing Prediction API...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logger.info("Shutting down Bike Sharing Prediction API...")


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    logger.warning("Running in development mode. Do not run like this in production.")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")