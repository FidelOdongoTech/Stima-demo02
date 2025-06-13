"""
Loan account model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

from .enums import LoanStatus


class LoanAccount(BaseModel):
    """Loan account model representing a member's loan."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_number: str
    member_id: str
    member_number: str
    loan_type: str  # "branch" or "mobile"
    principal_amount: float
    outstanding_balance: float
    monthly_payment: float
    interest_rate: float
    loan_term_months: int
    disbursement_date: datetime
    maturity_date: datetime
    last_payment_date: Optional[datetime] = None
    days_in_arrears: int = 0
    arrears_amount: float = 0.0
    status: LoanStatus
    branch_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def is_non_performing(self) -> bool:
        """Check if the loan is non-performing."""
        return self.status == LoanStatus.NON_PERFORMING

    @property
    def arrears_percentage(self) -> float:
        """Calculate arrears as percentage of outstanding balance."""
        if self.outstanding_balance == 0:
            return 0.0
        return (self.arrears_amount / self.outstanding_balance) * 100


class LoanAccountCreate(BaseModel):
    """Model for creating a new loan account."""
    
    loan_number: str
    member_id: str
    member_number: str
    loan_type: str
    principal_amount: float
    outstanding_balance: float
    monthly_payment: float
    interest_rate: float
    loan_term_months: int
    disbursement_date: datetime
    branch_code: str

