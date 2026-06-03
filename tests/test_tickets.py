from application import create_app
from models import db, Customer
from datetime import datetime
import unittest

class TestTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date(), phone="757-555-1234", address="123 Main St", password="test")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_ticket(self):
        ticket_payload = {
            "customer_id": 1,
            "booking_date": "2023-01-01",
            "days_required": 5,
            "issue_reported": "Car won't start",
            "jobs_done": "Replaced battery",
            "pickup_dropoff": True,
            "followup_reqd": False,
            "job_completed": False
        }
        response = self.client.post('/service-tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['issue_reported'], "Car won't start")

    def test_invalid_creation(self):
        ticket_payload = {
            "customer_id": 1,
            "booking_date": "2023-01-01",
            "days_required": 5,
            "issue_reported": "Car won't start"
        }
        response = self.client.post('/service-tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['jobs_done'], ['Missing data for required field.'])

    def test_get_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_ticket(self):
        ticket_payload = {
            "customer_id": 1,
            "booking_date": "2023-01-01",
            "days_required": 5,
            "issue_reported": "Car won't start",
            "jobs_done": "Replaced battery",
            "pickup_dropoff": True,
            "followup_reqd": False,
            "job_completed": False
        }
        self.client.post('/service-tickets/', json=ticket_payload)
        response = self.client.get('/service-tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['issue_reported'], "Car won't start")

    def test_edit_mechanics(self):
        ticket_payload = {
            "customer_id": 1,
            "booking_date": "2023-01-01",
            "days_required": 5,
            "issue_reported": "Car won't start",
            "jobs_done": "Replaced battery",
            "pickup_dropoff": True,
            "followup_reqd": False,
            "job_completed": False
        }
        self.client.post('/service-tickets/', json=ticket_payload)
        response = self.client.put('/service-tickets/1/edit', json={"add_ids": [], "remove_ids": []})
        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):
        ticket_payload = {
            "customer_id": 1,
            "booking_date": "2023-01-01",
            "days_required": 5,
            "issue_reported": "Car won't start",
            "jobs_done": "Replaced battery",
            "pickup_dropoff": True,
            "followup_reqd": False,
            "job_completed": False
        }
        self.client.post('/service-tickets/', json=ticket_payload)
        self.client.post('/inventory/', json={"part": "Brake Pads", "quantity": 50, "price": 100.00})
        response = self.client.put('/service-tickets/1/add-part/1')
        self.assertEqual(response.status_code, 200)