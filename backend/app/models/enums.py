"""
Enumeration types for the Stima Sacco Debt Management System.
"""

from enum import Enum


class LoanStatus(str, Enum):
    """Loan account status enumeration."""
    PERFORMING = "performing"
    NON_PERFORMING = "non_performing"
    DEFAULTED = "defaulted"
    CLOSED = "closed"


class CallStatus(str, Enum):
    """Call log status enumeration."""
    SUCCESSFUL = "successful"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
    DISCONNECTED = "disconnected"


class CallType(str, Enum):
    """Call type enumeration."""
    OUTBOUND = "outbound"
    INBOUND = "inbound"


class PromiseStatus(str, Enum):
    """Promise to pay status enumeration."""
    PENDING = "pending"
    KEPT = "kept"
    BROKEN = "broken"
    EXPIRED = "expired"


class PartnerType(str, Enum):
    """External partner type enumeration."""
    DEBT_COLLECTOR = "debt_collector"
    AUCTIONEER = "auctioneer"
    LEGAL_FIRM = "legal_firm"


class EscalationLevel(str, Enum):
    """Escalation level enumeration."""
    BRANCH = "branch"
    HEAD_OFFICE = "head_office"
    EXTERNAL_PARTNER = "external_partner"

