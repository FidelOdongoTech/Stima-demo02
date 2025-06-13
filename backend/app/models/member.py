"""
Member model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Member(BaseModel):
    """Member model representing a Sacco member."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    member_number: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    id_number: str
    address: str
    branch_code: str
    registration_date: datetime
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def full_name(self) -> str:
        """Get the member's full name."""
        return f"{self.first_name} {self.last_name}"


class MemberCreate(BaseModel):
    """Model for creating a new member."""
    
    member_number: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    id_number: str
    address: str
    branch_code: str

