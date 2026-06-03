from application import create_app
from models import db
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Frank Jones",
            "position": "Head of Service"
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Frank Jones")

    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "Frank Jones"
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['position'], ['Missing data for required field.'])

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_mechanic(self):
        self.client.post('/mechanics/', json={"name": "Frank Jones", "position": "Head of Service"})
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Frank Jones')

    def test_update_mechanic(self):
        self.client.post('/mechanics/', json={"name": "Frank Jones", "position": "Head of Service"})
        update_payload = {"name": "Updated Name", "position": "Head of Service"}
        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_delete_mechanic(self):
        self.client.post('/mechanics/', json={"name": "Frank Jones", "position": "Head of Service"})
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_sorted_by_tickets(self):
        response = self.client.get('/mechanics/sorted-by-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)