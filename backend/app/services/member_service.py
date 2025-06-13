"""
Member service for business logic operations.
"""

from typing import List, Optional
from ..models import Member, MemberCreate
from ..config import get_database


class MemberService:
    """Service class for member-related operations."""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.members

    async def get_members(
        self, 
        skip: int = 0, 
        limit: int = 50, 
        search: Optional[str] = None
    ) -> List[Member]:
        """Get members with optional search and pagination."""
        query = {}
        
        if search:
            query = {
                "$or": [
                    {"first_name": {"$regex": search, "$options": "i"}},
                    {"last_name": {"$regex": search, "$options": "i"}},
                    {"member_number": {"$regex": search, "$options": "i"}},
                    {"phone_number": {"$regex": search, "$options": "i"}}
                ]
            }
        
        members_data = await self.collection.find(query).skip(skip).limit(limit).to_list(limit)
        return [Member(**member) for member in members_data]

    async def get_member_by_id(self, member_id: str) -> Optional[Member]:
        """Get member by ID."""
        member_data = await self.collection.find_one({"id": member_id})
        return Member(**member_data) if member_data else None

    async def get_member_by_number(self, member_number: str) -> Optional[Member]:
        """Get member by member number."""
        member_data = await self.collection.find_one({"member_number": member_number})
        return Member(**member_data) if member_data else None

    async def create_member(self, member_data: MemberCreate) -> Member:
        """Create a new member."""
        from datetime import datetime
        
        member = Member(
            **member_data.dict(),
            registration_date=datetime.utcnow()
        )
        
        await self.collection.insert_one(member.dict())
        return member

    async def update_member(self, member_id: str, update_data: dict) -> Optional[Member]:
        """Update member information."""
        result = await self.collection.update_one(
            {"id": member_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_member_by_id(member_id)
        return None

    async def delete_member(self, member_id: str) -> bool:
        """Delete a member."""
        result = await self.collection.delete_one({"id": member_id})
        return result.deleted_count > 0

    async def get_total_members_count(self) -> int:
        """Get total count of members."""
        return await self.collection.count_documents({})

