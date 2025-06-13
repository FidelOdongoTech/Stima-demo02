"""
API routes package for the Stima Sacco Debt Management System.
"""

from fastapi import APIRouter
from .dashboard import router as dashboard_router
from .members import router as members_router
from .loans import router as loans_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(dashboard_router)
api_router.include_router(members_router)
api_router.include_router(loans_router)

__all__ = ["api_router"]

