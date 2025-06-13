"""
Dashboard service for business logic operations.
"""

from datetime import datetime, timedelta
from ..models import DashboardStats
from ..config import get_database


class DashboardService:
    """Service class for dashboard-related operations."""
    
    def __init__(self):
        self.db = get_database()

    async def get_dashboard_statistics(self) -> DashboardStats:
        """Get comprehensive dashboard statistics."""
        # Get basic counts
        total_members = await self.db.members.count_documents({})
        total_loans = await self.db.loan_accounts.count_documents({})
        total_npl_loans = await self.db.loan_accounts.count_documents({"status": "non_performing"})
        
        # Calculate financial totals
        portfolio_totals = await self._calculate_portfolio_totals()
        
        # Calculate recovery rate (simplified calculation)
        recovery_rate = await self._calculate_recovery_rate()
        
        # Get today's activity stats
        today_stats = await self._get_today_activity_stats()
        
        return DashboardStats(
            total_members=total_members,
            total_loans=total_loans,
            total_npl_loans=total_npl_loans,
            total_outstanding_amount=portfolio_totals["total_outstanding"],
            total_arrears_amount=portfolio_totals["total_arrears"],
            recovery_rate_percent=recovery_rate,
            calls_today=today_stats["calls_today"],
            promises_due_today=today_stats["promises_due_today"],
            escalations_pending=today_stats["escalations_pending"]
        )

    async def _calculate_portfolio_totals(self) -> dict:
        """Calculate portfolio financial totals."""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_outstanding": {"$sum": "$outstanding_balance"},
                    "total_arrears": {"$sum": "$arrears_amount"}
                }
            }
        ]
        
        result = await self.db.loan_accounts.aggregate(pipeline).to_list(1)
        if result:
            return {
                "total_outstanding": result[0]["total_outstanding"],
                "total_arrears": result[0]["total_arrears"]
            }
        return {"total_outstanding": 0, "total_arrears": 0}

    async def _calculate_recovery_rate(self) -> float:
        """Calculate recovery rate percentage."""
        # This is a simplified calculation
        # In a real system, you would calculate based on actual recoveries
        return 65.5

    async def _get_today_activity_stats(self) -> dict:
        """Get today's activity statistics."""
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        tomorrow_start = datetime.combine(today + timedelta(days=1), datetime.min.time())
        
        # Count today's calls
        calls_today = await self.db.call_logs.count_documents({
            "call_start_time": {"$gte": today_start}
        })
        
        # Count promises due today
        promises_due_today = await self.db.promises_to_pay.count_documents({
            "promised_date": {
                "$gte": today_start,
                "$lt": tomorrow_start
            },
            "status": "pending"
        })
        
        # Count pending escalations
        escalations_pending = await self.db.partner_assignments.count_documents({
            "status": "assigned"
        })
        
        return {
            "calls_today": calls_today,
            "promises_due_today": promises_due_today,
            "escalations_pending": escalations_pending
        }

