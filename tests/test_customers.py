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

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_customer(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_update_customer(self):
        update_payload = {
            "name": "Updated Name",
            "email": "test@email.com",
            "DOB": "1900-01-01",
            "phone": "757-555-1234",
            "address": "123 Main St",
            "password": "test"
        }
        response = self.client.put('/customers/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_delete_customer(self):
        response = self.client.delete('/customers/1')
        self.assertEqual(response.status_code, 200)

    def test_get_my_tickets(self):
        headers = {'Authorization': 'Bearer ' + self.token}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_delete_me(self):
        headers = {'Authorization': 'Bearer ' + self.token}
        response = self.client.delete('/customers/me', headers=headers)
        self.assertEqual(response.status_code, 200)