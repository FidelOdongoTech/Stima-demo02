"""
Dashboard API routes.
"""

from fastapi import APIRouter, Depends
from ..models import DashboardStats
from ..services import DashboardService
from ..utils import get_current_active_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_statistics(
    current_user: dict = Depends(get_current_active_user)
) -> DashboardStats:
    """
    Get comprehensive dashboard statistics.
    
    Returns key metrics including:
    - Total members and loans
    - NPL statistics
    - Financial totals
    - Today's activity metrics
    """
    dashboard_service = DashboardService()
    return await dashboard_service.get_dashboard_statistics()

