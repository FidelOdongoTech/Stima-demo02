"""
Loan API routes.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from ..models import LoanAccount, LoanAccountCreate
from ..services import LoanService
from ..utils import get_current_active_user

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("", response_model=List[LoanAccount])
async def get_loans(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = Query(None, description="Filter by loan status"),
    member_search: Optional[str] = Query(None, description="Search by member details"),
    current_user: dict = Depends(get_current_active_user)
) -> List[LoanAccount]:
    """
    Get loans with filters and pagination.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        status: Optional status filter (performing, non_performing, etc.)
        member_search: Optional search term for member details
        
    Returns:
        List of loans matching the criteria
    """
    loan_service = LoanService()
    return await loan_service.get_loans(
        skip=skip,
        limit=limit,
        status=status,
        member_search=member_search
    )


@router.get("/{loan_id}", response_model=LoanAccount)
async def get_loan(
    loan_id: str,
    current_user: dict = Depends(get_current_active_user)
) -> LoanAccount:
    """
    Get loan by ID.
    
    Args:
        loan_id: Unique identifier of the loan
        
    Returns:
        Loan details
        
    Raises:
        HTTPException: If loan is not found
    """
    loan_service = LoanService()
    loan = await loan_service.get_loan_by_id(loan_id)
    
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    return loan


@router.get("/member/{member_id}", response_model=List[LoanAccount])
async def get_member_loans(
    member_id: str,
    current_user: dict = Depends(get_current_active_user)
) -> List[LoanAccount]:
    """
    Get all loans for a specific member.
    
    Args:
        member_id: Unique identifier of the member
        
    Returns:
        List of loans for the member
    """
    loan_service = LoanService()
    return await loan_service.get_loans_by_member_id(member_id)


@router.post("", response_model=LoanAccount)
async def create_loan(
    loan_data: LoanAccountCreate,
    current_user: dict = Depends(get_current_active_user)
) -> LoanAccount:
    """
    Create a new loan account.
    
    Args:
        loan_data: Loan creation data
        
    Returns:
        Created loan details
    """
    loan_service = LoanService()
    return await loan_service.create_loan(loan_data)

