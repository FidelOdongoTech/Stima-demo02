import requests
import unittest
import json
from datetime import datetime, timedelta
import uuid

# Use the public endpoint for testing
BACKEND_URL = "https://3d980fcd-1a3c-4c01-ac39-22510b450724.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class DebtManagementSystemTests(unittest.TestCase):
    """Test suite for Stima Sacco Debt Management System API"""

    def test_01_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        print("\n🔍 Testing Dashboard Statistics API...")
        response = requests.get(f"{API_URL}/dashboard/stats")
        
        self.assertEqual(response.status_code, 200, "Dashboard stats API should return 200")
        data = response.json()
        
        # Verify expected fields are present
        expected_fields = [
            "total_members", "total_loans", "total_npl_loans", 
            "recovery_rate_percent", "total_outstanding_amount", 
            "total_arrears_amount", "calls_today", "promises_due_today",
            "escalations_pending"
        ]
        
        for field in expected_fields:
            self.assertIn(field, data, f"Dashboard stats should include {field}")
        
        # Verify data types and reasonable values
        self.assertIsInstance(data["total_members"], int, "Total members should be an integer")
        self.assertIsInstance(data["total_loans"], int, "Total loans should be an integer")
        self.assertIsInstance(data["total_npl_loans"], int, "Total NPL loans should be an integer")
        
        # Verify the numbers match what we expect from the dummy data
        self.assertGreaterEqual(data["total_members"], 1000, "Should have at least 1000 members")
        self.assertGreaterEqual(data["total_loans"], 1900, "Should have at least 1900 loans")
        self.assertGreaterEqual(data["total_npl_loans"], 600, "Should have at least 600 NPL loans")
        
        print("✅ Dashboard Statistics API test passed")

    def test_02_loans_listing(self):
        """Test loans listing endpoint"""
        print("\n🔍 Testing Loans Listing API...")
        response = requests.get(f"{API_URL}/loans")
        
        self.assertEqual(response.status_code, 200, "Loans listing API should return 200")
        loans = response.json()
        
        # Verify we have loans data
        self.assertIsInstance(loans, list, "Loans endpoint should return a list")
        self.assertGreater(len(loans), 0, "Loans list should not be empty")
        
        # Check first loan structure
        loan = loans[0]
        expected_loan_fields = [
            "id", "loan_number", "member_number", "branch_code", 
            "loan_type", "outstanding_balance", "arrears_amount", 
            "days_in_arrears", "status"
        ]
        
        for field in expected_loan_fields:
            self.assertIn(field, loan, f"Loan object should include {field}")
        
        # Test filtering by status
        status_response = requests.get(f"{API_URL}/loans?status=non_performing")
        self.assertEqual(status_response.status_code, 200, "Status filter should work")
        status_loans = status_response.json()
        
        # Verify all returned loans have non_performing status
        if len(status_loans) > 0:
            for loan in status_loans:
                self.assertEqual(loan["status"], "non_performing", 
                                "Status filter should only return non_performing loans")
        
        print("✅ Loans Listing API test passed")

    def test_03_profix_sync(self):
        """Test ProFIX sync endpoint"""
        print("\n🔍 Testing ProFIX Sync API...")
        # Get a loan ID first
        loans_response = requests.get(f"{API_URL}/loans")
        loans = loans_response.json()
        
        if len(loans) > 0:
            loan_id = loans[0]["id"]
            response = requests.get(f"{API_URL}/profix/sync/{loan_id}")
            
            self.assertEqual(response.status_code, 200, "ProFIX sync API should return 200")
            data = response.json()
            
            self.assertIn("message", data, "Response should include a message")
            self.assertIn("success", data, "Response should include success status")
            self.assertTrue(data["success"], "Sync should be successful")
        else:
            self.skipTest("No loans available to test ProFIX sync")
        
        print("✅ ProFIX Sync API test passed")

    def test_04_calls_api(self):
        """Test calls API endpoints"""
        print("\n🔍 Testing Calls API...")
        # Test call logs endpoint
        logs_response = requests.get(f"{API_URL}/calls?limit=20")
        self.assertEqual(logs_response.status_code, 200, "Call logs API should return 200")
        logs = logs_response.json()
        self.assertIsInstance(logs, list, "Call logs should be a list")
        
        # Test auto-dial endpoint
        dial_response = requests.get(f"{API_URL}/calls/auto-dial")
        self.assertEqual(dial_response.status_code, 200, "Auto-dial API should return 200")
        dial_data = dial_response.json()
        
        expected_dial_fields = ["member", "loan", "phone_number"]
        for field in expected_dial_fields:
            self.assertIn(field, dial_data, f"Auto-dial response should include {field}")
        
        # Test creating a call log
        call_data = {
            "loan_id": dial_data["loan"]["id"],
            "member_id": dial_data["member"]["id"],
            "call_type": "outbound",
            "phone_number": dial_data["phone_number"],
            "call_status": "successful",
            "notes": "Test call from API test",
            "agent_id": "test_agent",
            "agent_name": "Test Agent",
            "follow_up_required": False
        }
        
        create_response = requests.post(f"{API_URL}/calls", json=call_data)
        self.assertEqual(create_response.status_code, 201, "Call creation API should return 201")
        created_call = create_response.json()
        self.assertIn("id", created_call, "Created call should have an ID")
        
        print("✅ Calls API tests passed")

    def test_05_promises_api(self):
        """Test promises API endpoints"""
        print("\n🔍 Testing Promises API...")
        # Test promises listing
        list_response = requests.get(f"{API_URL}/promises")
        self.assertEqual(list_response.status_code, 200, "Promises listing API should return 200")
        promises = list_response.json()
        self.assertIsInstance(promises, list, "Promises should be a list")
        
        # Get a loan and member ID for creating a promise
        loans_response = requests.get(f"{API_URL}/loans")
        loans = loans_response.json()
        
        if len(loans) > 0:
            # Create a promise
            promise_data = {
                "loan_id": loans[0]["id"],
                "member_id": str(uuid.uuid4()),  # Using a random UUID as member_id
                "call_id": str(uuid.uuid4()),
                "promised_amount": 5000.0,
                "promised_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "notes": "Test promise from API test",
                "agent_id": "test_agent",
                "agent_name": "Test Agent"
            }
            
            create_response = requests.post(f"{API_URL}/promises", json=promise_data)
            self.assertEqual(create_response.status_code, 201, "Promise creation API should return 201")
            created_promise = create_response.json()
            self.assertIn("id", created_promise, "Created promise should have an ID")
            
            # Test updating promise status
            promise_id = created_promise["id"]
            update_response = requests.put(
                f"{API_URL}/promises/{promise_id}/status", 
                params={"status": "kept"}
            )
            self.assertEqual(update_response.status_code, 200, "Promise status update API should return 200")
            
            # Verify the status was updated
            get_response = requests.get(f"{API_URL}/promises?status=kept")
            kept_promises = get_response.json()
            found = False
            for promise in kept_promises:
                if promise["id"] == promise_id:
                    found = True
                    self.assertEqual(promise["status"], "kept", "Promise status should be updated to kept")
                    break
            
            self.assertTrue(found, "Updated promise should be found in kept promises list")
        else:
            self.skipTest("No loans available to test promises API")
        
        print("✅ Promises API tests passed")

    def test_06_partners_api(self):
        """Test partners API endpoints"""
        print("\n🔍 Testing Partners API...")
        # Test partners listing
        partners_response = requests.get(f"{API_URL}/partners")
        self.assertEqual(partners_response.status_code, 200, "Partners listing API should return 200")
        partners = partners_response.json()
        self.assertIsInstance(partners, list, "Partners should be a list")
        
        if len(partners) > 0:
            partner = partners[0]
            expected_partner_fields = [
                "id", "partner_name", "partner_type", "contact_person", 
                "email", "phone_number", "commission_rate", "is_active"
            ]
            
            for field in expected_partner_fields:
                self.assertIn(field, partner, f"Partner object should include {field}")
        
        # Test partner assignments
        assignments_response = requests.get(f"{API_URL}/partner-assignments")
        self.assertEqual(assignments_response.status_code, 200, "Partner assignments API should return 200")
        assignments = assignments_response.json()
        self.assertIsInstance(assignments, list, "Assignments should be a list")
        
        print("✅ Partners API tests passed")

    def test_07_reports_api(self):
        """Test reports API endpoints"""
        print("\n🔍 Testing Reports API...")
        # Test NPL summary report
        npl_response = requests.get(f"{API_URL}/reports/npl-summary")
        self.assertEqual(npl_response.status_code, 200, "NPL summary report API should return 200")
        npl_data = npl_response.json()
        self.assertIsInstance(npl_data, list, "NPL summary should be a list")
        
        if len(npl_data) > 0:
            branch_data = npl_data[0]
            expected_branch_fields = [
                "_id", "total_loans", "total_outstanding", 
                "total_arrears", "avg_days_arrears"
            ]
            
            for field in expected_branch_fields:
                self.assertIn(field, branch_data, f"Branch summary should include {field}")
        
        # Test collection performance report
        collection_response = requests.get(f"{API_URL}/reports/collection-performance")
        self.assertEqual(collection_response.status_code, 200, "Collection performance API should return 200")
        collection_data = collection_response.json()
        self.assertIsInstance(collection_data, list, "Collection performance should be a list")
        
        print("✅ Reports API tests passed")

    def test_08_notifications_api(self):
        """Test notifications API endpoints"""
        print("\n🔍 Testing Notifications API...")
        # Test notifications listing
        list_response = requests.get(f"{API_URL}/notifications")
        self.assertEqual(list_response.status_code, 200, "Notifications listing API should return 200")
        notifications = list_response.json()
        self.assertIsInstance(notifications, list, "Notifications should be a list")
        
        # Create a test notification
        notification_data = {
            "recipient_id": "test_user",
            "recipient_type": "agent",
            "notification_type": "payment_due",
            "title": "Test Notification",
            "message": "This is a test notification from API test",
            "is_read": False,
            "sent_at": datetime.now().isoformat()
        }
        
        create_response = requests.post(f"{API_URL}/notifications", json=notification_data)
        self.assertEqual(create_response.status_code, 201, "Notification creation API should return 201")
        created_notification = create_response.json()
        self.assertIn("id", created_notification, "Created notification should have an ID")
        
        # Test marking notification as read
        notification_id = created_notification["id"]
        read_response = requests.put(f"{API_URL}/notifications/{notification_id}/read")
        self.assertEqual(read_response.status_code, 200, "Mark as read API should return 200")
        
        # Verify notification was marked as read
        get_response = requests.get(f"{API_URL}/notifications?unread_only=false")
        all_notifications = get_response.json()
        found = False
        for notification in all_notifications:
            if notification["id"] == notification_id:
                found = True
                self.assertTrue(notification["is_read"], "Notification should be marked as read")
                self.assertIsNotNone(notification["read_at"], "Read timestamp should be set")
                break
        
        self.assertTrue(found, "Updated notification should be found in notifications list")
        
        print("✅ Notifications API tests passed")

if __name__ == "__main__":
    print("🧪 Starting Stima Sacco Debt Management System API Tests")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
