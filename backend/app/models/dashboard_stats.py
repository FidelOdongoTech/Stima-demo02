"""
Dashboard statistics model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel


class DashboardStats(BaseModel):
    """Dashboard statistics model."""
    
    total_members: int
    total_loans: int
    total_npl_loans: int
    total_outstanding_amount: float
    total_arrears_amount: float
    recovery_rate_percent: float
    calls_today: int
    promises_due_today: int
    escalations_pending: int

    @property
    def npl_percentage(self) -> float:
        """Calculate NPL percentage."""
        if self.total_loans == 0:
            return 0.0
        return (self.total_npl_loans / self.total_loans) * 100

    @property
    def arrears_percentage(self) -> float:
        """Calculate arrears as percentage of outstanding amount."""
        if self.total_outstanding_amount == 0:
            return 0.0
        return (self.total_arrears_amount / self.total_outstanding_amount) * 100

