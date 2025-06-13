"""
Custom exception classes for the Stima Sacco Debt Management System.
"""

from fastapi import HTTPException, status


class StimaException(Exception):
    """Base exception class for Stima Sacco application."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class MemberNotFoundException(StimaException):
    """Exception raised when a member is not found."""
    
    def __init__(self, member_id: str):
        message = f"Member with ID {member_id} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class LoanNotFoundException(StimaException):
    """Exception raised when a loan is not found."""
    
    def __init__(self, loan_id: str):
        message = f"Loan with ID {loan_id} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class DuplicateMemberException(StimaException):
    """Exception raised when attempting to create a duplicate member."""
    
    def __init__(self, member_number: str):
        message = f"Member with number {member_number} already exists"
        super().__init__(message, status.HTTP_409_CONFLICT)


class InvalidLoanStatusException(StimaException):
    """Exception raised when an invalid loan status transition is attempted."""
    
    def __init__(self, current_status: str, new_status: str):
        message = f"Cannot change loan status from {current_status} to {new_status}"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class DatabaseConnectionException(StimaException):
    """Exception raised when database connection fails."""
    
    def __init__(self):
        message = "Failed to connect to database"
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE)


class ExternalServiceException(StimaException):
    """Exception raised when external service integration fails."""
    
    def __init__(self, service_name: str, error_message: str):
        message = f"External service {service_name} error: {error_message}"
        super().__init__(message, status.HTTP_502_BAD_GATEWAY)

