"""
Loan service for business logic operations.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from ..models import LoanAccount, LoanAccountCreate, LoanStatus
from ..config import get_database


class LoanService:
    """Service class for loan-related operations."""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.loan_accounts

    async def get_loans(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None,
        member_search: Optional[str] = None
    ) -> List[LoanAccount]:
        """Get loans with filters and pagination."""
        query = {}
        
        if status:
            query["status"] = status
            
        if member_search:
            # Find members first, then filter loans
            members_collection = self.db.members
            members = await members_collection.find({
                "$or": [
                    {"first_name": {"$regex": member_search, "$options": "i"}},
                    {"last_name": {"$regex": member_search, "$options": "i"}},
                    {"member_number": {"$regex": member_search, "$options": "i"}}
                ]
            }).to_list(None)
            
            member_ids = [member["id"] for member in members]
            if member_ids:
                query["member_id"] = {"$in": member_ids}
            else:
                # No matching members found
                return []
        
        loans_data = await self.collection.find(query).skip(skip).limit(limit).to_list(limit)
        return [LoanAccount(**loan) for loan in loans_data]

    async def get_loan_by_id(self, loan_id: str) -> Optional[LoanAccount]:
        """Get loan by ID."""
        loan_data = await self.collection.find_one({"id": loan_id})
        return LoanAccount(**loan_data) if loan_data else None

    async def get_loans_by_member_id(self, member_id: str) -> List[LoanAccount]:
        """Get all loans for a specific member."""
        loans_data = await self.collection.find({"member_id": member_id}).to_list(None)
        return [LoanAccount(**loan) for loan in loans_data]

    async def create_loan(self, loan_data: LoanAccountCreate) -> LoanAccount:
        """Create a new loan account."""
        # Calculate maturity date
        maturity_date = loan_data.disbursement_date + timedelta(
            days=loan_data.loan_term_months * 30
        )
        
        loan = LoanAccount(
            **loan_data.dict(),
            maturity_date=maturity_date,
            status=LoanStatus.PERFORMING
        )
        
        await self.collection.insert_one(loan.dict())
        return loan

    async def update_loan(self, loan_id: str, update_data: dict) -> Optional[LoanAccount]:
        """Update loan information."""
        result = await self.collection.update_one(
            {"id": loan_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_loan_by_id(loan_id)
        return None

    async def get_npl_loans(self, skip: int = 0, limit: int = 50) -> List[LoanAccount]:
        """Get non-performing loans."""
        return await self.get_loans(
            skip=skip,
            limit=limit,
            status=LoanStatus.NON_PERFORMING
        )

    async def get_total_loans_count(self) -> int:
        """Get total count of loans."""
        return await self.collection.count_documents({})

    async def get_npl_loans_count(self) -> int:
        """Get count of non-performing loans."""
        return await self.collection.count_documents({"status": LoanStatus.NON_PERFORMING})

    async def calculate_portfolio_totals(self) -> dict:
        """Calculate portfolio totals."""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_outstanding": {"$sum": "$outstanding_balance"},
                    "total_arrears": {"$sum": "$arrears_amount"}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(1)
        if result:
            return {
                "total_outstanding": result[0]["total_outstanding"],
                "total_arrears": result[0]["total_arrears"]
            }
        return {"total_outstanding": 0, "total_arrears": 0}

