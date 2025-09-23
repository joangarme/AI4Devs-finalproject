"""
Main entry point for the Personal Finance Tracker API.

This module contains the FastAPI application instance with configuration
loaded from environment variables.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

# Get application settings
settings = get_settings()

# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for personal finance tracking and management",
    debug=settings.debug
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status information about the API
    """
    return {
        "status": "healthy",
        "message": f"{settings.app_name} is running",
        "version": "0.1.0",
        "debug": settings.debug,
        "log_level": settings.log_level
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        log_level=settings.log_level.lower()
    )
