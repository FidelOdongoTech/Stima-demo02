"""
Call log model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

from .enums import CallType, CallStatus


class CallLog(BaseModel):
    """Call log model representing a call made to a member."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_id: str
    member_id: str
    call_type: CallType
    phone_number: str
    call_start_time: datetime
    call_end_time: Optional[datetime] = None
    call_duration_seconds: Optional[int] = None
    call_status: CallStatus
    notes: str = ""
    agent_id: str
    agent_name: str
    recording_url: Optional[str] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def call_duration_minutes(self) -> Optional[float]:
        """Get call duration in minutes."""
        if self.call_duration_seconds is None:
            return None
        return self.call_duration_seconds / 60

    @property
    def was_successful(self) -> bool:
        """Check if the call was successful."""
        return self.call_status == CallStatus.SUCCESSFUL


class CallLogCreate(BaseModel):
    """Model for creating a new call log."""
    
    loan_id: str
    member_id: str
    call_type: CallType
    phone_number: str
    call_status: CallStatus
    notes: str = ""
    agent_id: str
    agent_name: str
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None

