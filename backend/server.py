from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
from enum import Enum
import random
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Stima Sacco Debt Management System", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Enums
class LoanStatus(str, Enum):
    PERFORMING = "performing"
    NON_PERFORMING = "non_performing"
    DEFAULTED = "defaulted"
    CLOSED = "closed"

class CallStatus(str, Enum):
    SUCCESSFUL = "successful"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
    DISCONNECTED = "disconnected"

class CallType(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"

class PromiseStatus(str, Enum):
    PENDING = "pending"
    KEPT = "kept"
    BROKEN = "broken"
    EXPIRED = "expired"

class PartnerType(str, Enum):
    DEBT_COLLECTOR = "debt_collector"
    AUCTIONEER = "auctioneer"
    LEGAL_FIRM = "legal_firm"

class EscalationLevel(str, Enum):
    BRANCH = "branch"
    HEAD_OFFICE = "head_office"
    EXTERNAL_PARTNER = "external_partner"

# Models
class Member(BaseModel):
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

class MemberCreate(BaseModel):
    member_number: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    id_number: str
    address: str
    branch_code: str

class LoanAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_number: str
    member_id: str
    member_number: str
    loan_type: str  # "branch" or "mobile"
    principal_amount: float
    outstanding_balance: float
    monthly_payment: float
    interest_rate: float
    loan_term_months: int
    disbursement_date: datetime
    maturity_date: datetime
    last_payment_date: Optional[datetime] = None
    days_in_arrears: int = 0
    arrears_amount: float = 0.0
    status: LoanStatus
    branch_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LoanAccountCreate(BaseModel):
    loan_number: str
    member_id: str
    member_number: str
    loan_type: str
    principal_amount: float
    outstanding_balance: float
    monthly_payment: float
    interest_rate: float
    loan_term_months: int
    disbursement_date: datetime
    branch_code: str

class CallLog(BaseModel):
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

class CallLogCreate(BaseModel):
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

class PromiseToPay(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_id: str
    member_id: str
    call_id: str
    promised_amount: float
    promised_date: datetime
    status: PromiseStatus
    notes: str = ""
    agent_id: str
    agent_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PromiseToPayCreate(BaseModel):
    loan_id: str
    member_id: str
    call_id: str
    promised_amount: float
    promised_date: datetime
    notes: str = ""
    agent_id: str
    agent_name: str

class ExternalPartner(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    partner_name: str
    partner_type: PartnerType
    contact_person: str
    email: str
    phone_number: str
    commission_rate: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExternalPartnerCreate(BaseModel):
    partner_name: str
    partner_type: PartnerType
    contact_person: str
    email: str
    phone_number: str
    commission_rate: float

class PartnerAssignment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    loan_id: str
    partner_id: str
    assigned_date: datetime
    expected_recovery_amount: float
    actual_recovery_amount: float = 0.0
    commission_amount: float = 0.0
    status: str = "assigned"  # assigned, in_progress, completed, failed
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PartnerAssignmentCreate(BaseModel):
    loan_id: str
    partner_id: str
    expected_recovery_amount: float
    notes: str = ""

class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recipient_id: str
    recipient_type: str  # member, agent, partner
    notification_type: str  # payment_due, promise_due, escalation
    title: str
    message: str
    is_read: bool = False
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

class DashboardStats(BaseModel):
    total_members: int
    total_loans: int
    total_npl_loans: int
    total_outstanding_amount: float
    total_arrears_amount: float
    recovery_rate_percent: float
    calls_today: int
    promises_due_today: int
    escalations_pending: int

# Authentication dependency (simplified for demo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In a real system, you would validate the JWT token here
    return {"user_id": "demo_user", "name": "Demo Agent", "role": "agent"}

# Helper function to generate dummy data
async def generate_dummy_data():
    """Generate realistic dummy data for the system"""
    
    # Check if data already exists
    member_count = await db.members.count_documents({})
    if member_count > 0:
        return
    
    print("Generating dummy data...")
    
    # Generate Members (sample of 1000 members for demo)
    members = []
    kenyan_names = [
        ("John", "Kamau"), ("Mary", "Wanjiku"), ("Peter", "Mwangi"), ("Grace", "Akinyi"),
        ("David", "Kiprotich"), ("Agnes", "Nyong'o"), ("Samuel", "Ochieng"), ("Faith", "Wambui"),
        ("Michael", "Ruto"), ("Joyce", "Chebet"), ("Joseph", "Mutua"), ("Esther", "Wairimu"),
        ("Daniel", "Kinyua"), ("Rose", "Atieno"), ("Francis", "Mburu"), ("Lucy", "Jepkoech")
    ]
    
    branch_codes = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]
    
    for i in range(1000):
        first_name, last_name = random.choice(kenyan_names)
        member = Member(
            member_number=f"STM{10000 + i}",
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}@email.com",
            phone_number=f"+254{random.randint(700000000, 799999999)}",
            id_number=f"{random.randint(10000000, 39999999)}",
            address=f"P.O. Box {random.randint(1, 9999)}, Nairobi",
            branch_code=random.choice(branch_codes),
            registration_date=datetime.utcnow() - timedelta(days=random.randint(30, 1825))
        )
        members.append(member.dict())
    
    await db.members.insert_many(members)
    
    # Generate Loan Accounts
    members_list = await db.members.find().to_list(1000)
    loans = []
    
    for i, member in enumerate(members_list):
        # Each member can have 1-3 loans
        num_loans = random.randint(1, 3)
        
        for j in range(num_loans):
            loan_type = random.choice(["branch", "mobile"])
            principal = random.randint(50000, 2000000)  # 50K to 2M KES
            interest_rate = random.uniform(12.0, 24.0)
            term_months = random.choice([6, 12, 18, 24, 36])
            
            disbursement_date = datetime.utcnow() - timedelta(days=random.randint(30, 730))
            maturity_date = disbursement_date + timedelta(days=term_months * 30)
            
            # Calculate if loan should be NPL (35,000 out of 107,000 total)
            is_npl = random.random() < 0.33  # About 33% NPL rate
            
            if is_npl:
                days_in_arrears = random.randint(90, 730)  # 3 months to 2 years
                outstanding_balance = principal * random.uniform(0.6, 1.2)
                arrears_amount = outstanding_balance * random.uniform(0.3, 0.8)
                status = LoanStatus.NON_PERFORMING
                last_payment_date = datetime.utcnow() - timedelta(days=days_in_arrears)
            else:
                days_in_arrears = random.randint(0, 30)
                outstanding_balance = principal * random.uniform(0.2, 0.8)
                arrears_amount = 0.0
                status = LoanStatus.PERFORMING
                last_payment_date = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            
            monthly_payment = (principal / term_months) * (1 + interest_rate/100/12)
            
            loan = LoanAccount(
                loan_number=f"LN{member['member_number']}{j+1:02d}",
                member_id=member['id'],
                member_number=member['member_number'],
                loan_type=loan_type,
                principal_amount=principal,
                outstanding_balance=outstanding_balance,
                monthly_payment=monthly_payment,
                interest_rate=interest_rate,
                loan_term_months=term_months,
                disbursement_date=disbursement_date,
                maturity_date=maturity_date,
                last_payment_date=last_payment_date,
                days_in_arrears=days_in_arrears,
                arrears_amount=arrears_amount,
                status=status,
                branch_code=member['branch_code']
            )
            loans.append(loan.dict())
    
    await db.loan_accounts.insert_many(loans)
    
    # Generate External Partners
    partners = [
        ExternalPartner(
            partner_name="Elite Recovery Services",
            partner_type=PartnerType.DEBT_COLLECTOR,
            contact_person="Jane Doe",
            email="jane@eliterecovery.co.ke",
            phone_number="+254701234567",
            commission_rate=15.0
        ),
        ExternalPartner(
            partner_name="Quick Auction House",
            partner_type=PartnerType.AUCTIONEER,
            contact_person="Robert Smith",
            email="robert@quickauction.co.ke",
            phone_number="+254702345678",
            commission_rate=10.0
        ),
        ExternalPartner(
            partner_name="Legal Associates LLP",
            partner_type=PartnerType.LEGAL_FIRM,
            contact_person="Mary Johnson",
            email="mary@legalassociates.co.ke",
            phone_number="+254703456789",
            commission_rate=20.0
        )
    ]
    
    await db.external_partners.insert_many([p.dict() for p in partners])
    
    print("Dummy data generated successfully!")

# Initialize dummy data on startup
@app.on_event("startup")
async def startup_event():
    await generate_dummy_data()

# Dashboard API
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    total_members = await db.members.count_documents({})
    total_loans = await db.loan_accounts.count_documents({})
    total_npl_loans = await db.loan_accounts.count_documents({"status": "non_performing"})
    
    # Calculate totals
    pipeline = [
        {"$group": {
            "_id": None,
            "total_outstanding": {"$sum": "$outstanding_balance"},
            "total_arrears": {"$sum": "$arrears_amount"}
        }}
    ]
    result = await db.loan_accounts.aggregate(pipeline).to_list(1)
    total_outstanding = result[0]["total_outstanding"] if result else 0
    total_arrears = result[0]["total_arrears"] if result else 0
    
    # Calculate recovery rate (dummy calculation)
    recovery_rate = 65.5
    
    # Get today's stats
    today = datetime.utcnow().date()
    calls_today = await db.call_logs.count_documents({
        "call_start_time": {"$gte": datetime.combine(today, datetime.min.time())}
    })
    
    promises_due_today = await db.promises_to_pay.count_documents({
        "promised_date": {"$gte": datetime.combine(today, datetime.min.time()),
                         "$lt": datetime.combine(today + timedelta(days=1), datetime.min.time())},
        "status": "pending"
    })
    
    escalations_pending = await db.partner_assignments.count_documents({"status": "assigned"})
    
    return DashboardStats(
        total_members=total_members,
        total_loans=total_loans,
        total_npl_loans=total_npl_loans,
        total_outstanding_amount=total_outstanding,
        total_arrears_amount=total_arrears,
        recovery_rate_percent=recovery_rate,
        calls_today=calls_today,
        promises_due_today=promises_due_today,
        escalations_pending=escalations_pending
    )

# Member APIs
@api_router.get("/members", response_model=List[Member])
async def get_members(skip: int = 0, limit: int = 50, search: str = Query(None)):
    """Get members with optional search"""
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
    
    members = await db.members.find(query).skip(skip).limit(limit).to_list(limit)
    return [Member(**member) for member in members]

@api_router.get("/members/{member_id}", response_model=Member)
async def get_member(member_id: str):
    """Get member by ID"""
    member = await db.members.find_one({"id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return Member(**member)

@api_router.post("/members", response_model=Member)
async def create_member(member_data: MemberCreate):
    """Create new member"""
    member = Member(**member_data.dict(), registration_date=datetime.utcnow())
    await db.members.insert_one(member.dict())
    return member

# Loan Account APIs
@api_router.get("/loans", response_model=List[LoanAccount])
async def get_loans(skip: int = 0, limit: int = 50, status: str = Query(None), member_search: str = Query(None)):
    """Get loan accounts with filters"""
    query = {}
    if status:
        query["status"] = status
    if member_search:
        # Find members first, then filter loans
        members = await db.members.find({
            "$or": [
                {"first_name": {"$regex": member_search, "$options": "i"}},
                {"last_name": {"$regex": member_search, "$options": "i"}},
                {"member_number": {"$regex": member_search, "$options": "i"}}
            ]
        }).to_list(100)
        member_ids = [m["id"] for m in members]
        if member_ids:
            query["member_id"] = {"$in": member_ids}
        else:
            return []
    
    loans = await db.loan_accounts.find(query).skip(skip).limit(limit).to_list(limit)
    return [LoanAccount(**loan) for loan in loans]

@api_router.get("/loans/{loan_id}", response_model=LoanAccount)
async def get_loan(loan_id: str):
    """Get loan by ID"""
    loan = await db.loan_accounts.find_one({"id": loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return LoanAccount(**loan)

@api_router.get("/loans/{loan_id}/member", response_model=Member)
async def get_loan_member(loan_id: str):
    """Get member details for a loan"""
    loan = await db.loan_accounts.find_one({"id": loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    member = await db.members.find_one({"id": loan["member_id"]})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return Member(**member)

# Call Management APIs
@api_router.get("/calls", response_model=List[CallLog])
async def get_calls(skip: int = 0, limit: int = 50, loan_id: str = Query(None)):
    """Get call logs"""
    query = {}
    if loan_id:
        query["loan_id"] = loan_id
    
    calls = await db.call_logs.find(query).sort("call_start_time", -1).skip(skip).limit(limit).to_list(limit)
    return [CallLog(**call) for call in calls]

@api_router.post("/calls", response_model=CallLog)
async def create_call_log(call_data: CallLogCreate, current_user: dict = Depends(get_current_user)):
    """Create new call log"""
    call_log = CallLog(
        **call_data.dict(),
        call_start_time=datetime.utcnow(),
        agent_id=current_user["user_id"],
        agent_name=current_user["name"]
    )
    
    # Simulate call duration for completed calls
    if call_data.call_status == CallStatus.SUCCESSFUL:
        call_log.call_end_time = datetime.utcnow() + timedelta(minutes=random.randint(2, 15))
        call_log.call_duration_seconds = random.randint(120, 900)
        call_log.recording_url = f"https://recordings.stimasacco.co.ke/{call_log.id}.mp3"
    
    await db.call_logs.insert_one(call_log.dict())
    return call_log

@api_router.get("/calls/auto-dial")
async def auto_dial_next():
    """Auto dial next NPL customer"""
    # Find next NPL loan without recent call
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    # Get NPL loans that haven't been called in the last 24 hours
    pipeline = [
        {"$match": {"status": "non_performing"}},
        {"$lookup": {
            "from": "call_logs",
            "localField": "id",
            "foreignField": "loan_id",
            "as": "recent_calls"
        }},
        {"$match": {
            "$or": [
                {"recent_calls": {"$size": 0}},
                {"recent_calls.call_start_time": {"$lt": yesterday}}
            ]
        }},
        {"$limit": 1}
    ]
    
    loans = await db.loan_accounts.aggregate(pipeline).to_list(1)
    if not loans:
        raise HTTPException(status_code=404, detail="No loans available for auto dial")
    
    loan = loans[0]
    member = await db.members.find_one({"id": loan["member_id"]})
    
    return {
        "loan": LoanAccount(**loan),
        "member": Member(**member),
        "phone_number": member["phone_number"],
        "message": "Ready to dial. Click 'Start Call' to begin."
    }

# Promise to Pay APIs
@api_router.get("/promises", response_model=List[PromiseToPay])
async def get_promises(skip: int = 0, limit: int = 50, status: str = Query(None)):
    """Get promise to pay records"""
    query = {}
    if status:
        query["status"] = status
    
    promises = await db.promises_to_pay.find(query).sort("promised_date", 1).skip(skip).limit(limit).to_list(limit)
    return [PromiseToPay(**promise) for promise in promises]

@api_router.post("/promises", response_model=PromiseToPay)
async def create_promise(promise_data: PromiseToPayCreate, current_user: dict = Depends(get_current_user)):
    """Create new promise to pay"""
    promise = PromiseToPay(
        **promise_data.dict(),
        status=PromiseStatus.PENDING,
        agent_id=current_user["user_id"],
        agent_name=current_user["name"]
    )
    await db.promises_to_pay.insert_one(promise.dict())
    return promise

@api_router.put("/promises/{promise_id}/status")
async def update_promise_status(promise_id: str, status: PromiseStatus):
    """Update promise status"""
    result = await db.promises_to_pay.update_one(
        {"id": promise_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Promise not found")
    return {"message": "Promise status updated"}

# External Partner APIs
@api_router.get("/partners", response_model=List[ExternalPartner])
async def get_partners():
    """Get external partners"""
    partners = await db.external_partners.find({"is_active": True}).to_list(100)
    return [ExternalPartner(**partner) for partner in partners]

@api_router.post("/partners", response_model=ExternalPartner)
async def create_partner(partner_data: ExternalPartnerCreate):
    """Create new external partner"""
    partner = ExternalPartner(**partner_data.dict())
    await db.external_partners.insert_one(partner.dict())
    return partner

@api_router.get("/partner-assignments", response_model=List[PartnerAssignment])
async def get_partner_assignments(skip: int = 0, limit: int = 50):
    """Get partner assignments"""
    assignments = await db.partner_assignments.find().sort("assigned_date", -1).skip(skip).limit(limit).to_list(limit)
    return [PartnerAssignment(**assignment) for assignment in assignments]

@api_router.post("/partner-assignments", response_model=PartnerAssignment)
async def create_partner_assignment(assignment_data: PartnerAssignmentCreate):
    """Assign loan to external partner"""
    assignment = PartnerAssignment(
        **assignment_data.dict(),
        assigned_date=datetime.utcnow()
    )
    await db.partner_assignments.insert_one(assignment.dict())
    return assignment

# Notification APIs
@api_router.get("/notifications", response_model=List[Notification])
async def get_notifications(skip: int = 0, limit: int = 20, unread_only: bool = False):
    """Get notifications"""
    query = {}
    if unread_only:
        query["is_read"] = False
    
    notifications = await db.notifications.find(query).sort("sent_at", -1).skip(skip).limit(limit).to_list(limit)
    return [Notification(**notification) for notification in notifications]

@api_router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str):
    """Mark notification as read"""
    result = await db.notifications.update_one(
        {"id": notification_id},
        {"$set": {"is_read": True, "read_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}

# Reporting APIs
@api_router.get("/reports/npl-summary")
async def get_npl_summary():
    """Get NPL summary report"""
    pipeline = [
        {"$match": {"status": "non_performing"}},
        {"$group": {
            "_id": "$branch_code",
            "total_loans": {"$sum": 1},
            "total_outstanding": {"$sum": "$outstanding_balance"},
            "total_arrears": {"$sum": "$arrears_amount"},
            "avg_days_arrears": {"$avg": "$days_in_arrears"}
        }},
        {"$sort": {"total_outstanding": -1}}
    ]
    
    results = await db.loan_accounts.aggregate(pipeline).to_list(100)
    return results

@api_router.get("/reports/collection-performance")
async def get_collection_performance():
    """Get collection performance report"""
    # Simulate collection performance data
    today = datetime.utcnow()
    last_30_days = today - timedelta(days=30)
    
    pipeline = [
        {"$match": {"promised_date": {"$gte": last_30_days}}},
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "total_amount": {"$sum": "$promised_amount"}
        }}
    ]
    
    results = await db.promises_to_pay.aggregate(pipeline).to_list(100)
    return results

# ProFIX Integration Simulation
@api_router.get("/profix/sync/{loan_id}")
async def sync_with_profix(loan_id: str):
    """Simulate ProFIX data synchronization"""
    loan = await db.loan_accounts.find_one({"id": loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Simulate fetching updated data from ProFIX
    await asyncio.sleep(1)  # Simulate API call delay
    
    # Update with simulated new data
    updated_balance = loan["outstanding_balance"] * random.uniform(0.95, 1.02)
    result = await db.loan_accounts.update_one(
        {"id": loan_id},
        {"$set": {"outstanding_balance": updated_balance, "updated_at": datetime.utcnow()}}
    )
    
    return {
        "message": "Loan data synchronized with ProFIX",
        "loan_id": loan_id,
        "updated_balance": updated_balance,
        "sync_time": datetime.utcnow(),
        "success": True
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
