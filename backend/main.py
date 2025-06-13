"""
Main FastAPI application for the Stima Sacco Debt Management System.

This is the refactored version with improved structure, separation of concerns,
and better maintainability.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from pathlib import Path

from app.config import app_config, close_database_connection
from app.routes import api_router
from app.services.data_generator import DataGeneratorService
from app.utils import setup_logging, get_logger, StimaException
from app.utils.exception_handlers import (
    stima_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

# Configure logging
setup_logging(app_config.LOG_LEVEL)
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=app_config.API_TITLE,
    version=app_config.API_VERSION,
    description="A comprehensive debt management system for Stima Sacco with improved architecture and maintainability"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(StimaException, stima_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
app.include_router(api_router, prefix=app_config.API_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Stima Sacco Debt Management System...")
    logger.info(f"Environment: {app_config.LOG_LEVEL}")
    logger.info(f"Database: {app_config.DATABASE_NAME}")
    
    try:
        # Generate dummy data if needed
        data_generator = DataGeneratorService()
        await data_generator.generate_dummy_data_if_needed()
        
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Stima Sacco Debt Management System...")
    
    try:
        await close_database_connection()
        logger.info("Application shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Stima Sacco Debt Management System API",
        "version": app_config.API_VERSION,
        "status": "healthy",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "stima-sacco-debt-management",
        "version": app_config.API_VERSION,
        "environment": app_config.LOG_LEVEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=app_config.LOG_LEVEL.lower()
    )

