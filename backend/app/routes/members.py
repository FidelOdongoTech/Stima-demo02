"""
Member API routes.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from ..models import Member, MemberCreate
from ..services import MemberService
from ..utils import get_current_active_user

router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=List[Member])
async def get_members(
    skip: int = 0,
    limit: int = 50,
    search: str = Query(None, description="Search by name, member number, or phone"),
    current_user: dict = Depends(get_current_active_user)
) -> List[Member]:
    """
    Get members with optional search and pagination.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        search: Optional search term for filtering members
        
    Returns:
        List of members matching the criteria
    """
    member_service = MemberService()
    return await member_service.get_members(skip=skip, limit=limit, search=search)


@router.get("/{member_id}", response_model=Member)
async def get_member(
    member_id: str,
    current_user: dict = Depends(get_current_active_user)
) -> Member:
    """
    Get member by ID.
    
    Args:
        member_id: Unique identifier of the member
        
    Returns:
        Member details
        
    Raises:
        HTTPException: If member is not found
    """
    member_service = MemberService()
    member = await member_service.get_member_by_id(member_id)
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return member


@router.post("", response_model=Member)
async def create_member(
    member_data: MemberCreate,
    current_user: dict = Depends(get_current_active_user)
) -> Member:
    """
    Create a new member.
    
    Args:
        member_data: Member creation data
        
    Returns:
        Created member details
    """
    member_service = MemberService()
    return await member_service.create_member(member_data)

