from application import create_app
from models import db, Customer
from datetime import datetime
from application.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date(), phone="757-555-1234", address="123 Main St", password="test")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "phone": "757-555-1234",
            "address": "123 Main St",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')