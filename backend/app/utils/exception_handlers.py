"""
Global exception handler for the FastAPI application.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from ..utils.exceptions import StimaException

logger = logging.getLogger(__name__)


async def stima_exception_handler(request: Request, exc: StimaException):
    """Handle custom Stima exceptions."""
    logger.error(f"Stima exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Application Error",
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    logger.error(f"Validation exception: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid input data",
            "details": exc.errors(),
            "status_code": 422
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )

