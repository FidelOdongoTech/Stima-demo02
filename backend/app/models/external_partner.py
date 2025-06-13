"""
External partner model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from .enums import PartnerType


class ExternalPartner(BaseModel):
    """External partner model representing debt collection partners."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    partner_name: str
    partner_type: PartnerType
    contact_person: str
    email: str
    phone_number: str
    commission_rate: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def commission_percentage(self) -> str:
        """Get commission rate as a formatted percentage."""
        return f"{self.commission_rate}%"


class ExternalPartnerCreate(BaseModel):
    """Model for creating a new external partner."""
    
    partner_name: str
    partner_type: PartnerType
    contact_person: str
    email: str
    phone_number: str
    commission_rate: float

