"""
Notification model for the Stima Sacco Debt Management System.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Notification(BaseModel):
    """Notification model representing system notifications."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recipient_id: str
    recipient_type: str  # member, agent, partner
    notification_type: str  # payment_due, promise_due, escalation
    title: str
    message: str
    is_read: bool = False
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

    @property
    def is_unread(self) -> bool:
        """Check if notification is unread."""
        return not self.is_read

    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()

