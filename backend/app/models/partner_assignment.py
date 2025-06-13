"""
Partner assignment model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class PartnerAssignment(BaseModel):
    """Partner assignment model representing loan assignments to external partners."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_id: str
    partner_id: str
    assigned_date: datetime
    expected_recovery_amount: float
    actual_recovery_amount: float = 0.0
    commission_amount: float = 0.0
    status: str = "assigned"  # assigned, in_progress, completed, failed
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def recovery_percentage(self) -> float:
        """Calculate recovery percentage."""
        if self.expected_recovery_amount == 0:
            return 0.0
        return (self.actual_recovery_amount / self.expected_recovery_amount) * 100

    @property
    def is_completed(self) -> bool:
        """Check if assignment is completed."""
        return self.status == "completed"


class PartnerAssignmentCreate(BaseModel):
    """Model for creating a new partner assignment."""
    
    loan_id: str
    partner_id: str
    expected_recovery_amount: float
    notes: str = ""

