"""
Promise to pay model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from .enums import PromiseStatus


class PromiseToPay(BaseModel):
    """Promise to pay model representing a member's payment commitment."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_id: str
    member_id: str
    call_id: str
    promised_amount: float
    promised_date: datetime
    status: PromiseStatus
    notes: str = ""
    agent_id: str
    agent_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def is_overdue(self) -> bool:
        """Check if the promise is overdue."""
        return (
            self.status == PromiseStatus.PENDING 
            and self.promised_date < datetime.utcnow()
        )

    @property
    def days_until_due(self) -> int:
        """Calculate days until promise is due."""
        delta = self.promised_date - datetime.utcnow()
        return delta.days


class PromiseToPayCreate(BaseModel):
    """Model for creating a new promise to pay."""
    
    loan_id: str
    member_id: str
    call_id: str
    promised_amount: float
    promised_date: datetime
    notes: str = ""
    agent_id: str
    agent_name: str

