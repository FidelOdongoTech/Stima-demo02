"""
Data generation service for creating dummy data.
"""

import random
from datetime import datetime, timedelta
from typing import List

from ..models import Member, LoanAccount, ExternalPartner, LoanStatus, PartnerType
from ..config import get_database


class DataGeneratorService:
    """Service for generating realistic dummy data."""
    
    def __init__(self):
        self.db = get_database()

    async def generate_dummy_data_if_needed(self):
        """Generate dummy data if the database is empty."""
        member_count = await self.db.members.count_documents({})
        if member_count > 0:
            return
        
        print("Generating dummy data...")
        await self._generate_members()
        await self._generate_loans()
        await self._generate_external_partners()
        print("Dummy data generated successfully!")

    async def _generate_members(self):
        """Generate dummy members."""
        kenyan_names = [
            ("John", "Kamau"), ("Mary", "Wanjiku"), ("Peter", "Mwangi"), ("Grace", "Akinyi"),
            ("David", "Kiprotich"), ("Agnes", "Nyong'o"), ("Samuel", "Ochieng"), ("Faith", "Wambui"),
            ("Michael", "Ruto"), ("Joyce", "Chebet"), ("Joseph", "Mutua"), ("Esther", "Wairimu"),
            ("Daniel", "Kinyua"), ("Rose", "Atieno"), ("Francis", "Mburu"), ("Lucy", "Jepkoech")
        ]
        
        branch_codes = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]
        
        members = []
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
        
        await self.db.members.insert_many(members)

    async def _generate_loans(self):
        """Generate dummy loan accounts."""
        members_list = await self.db.members.find().to_list(1000)
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
                
                # Calculate if loan should be NPL (33% NPL rate)
                is_npl = random.random() < 0.33
                
                if is_npl:
                    days_in_arrears = random.randint(90, 730)
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
        
        await self.db.loan_accounts.insert_many(loans)

    async def _generate_external_partners(self):
        """Generate dummy external partners."""
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
        
        await self.db.external_partners.insert_many([p.dict() for p in partners])

