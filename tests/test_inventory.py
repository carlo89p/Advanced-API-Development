from app import create_app
from models import db
import unittest

# class Inventory(db.Model):
#     __tablename__ = 'inventory'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     part: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     quantity: Mapped[int] = mapped_column(nullable=False)
#     price: Mapped[float] = mapped_column(nullable=False)

#     service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=ticket_inventory, back_populates='inventory')

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_inventory_item(self):
        inventory_payload = {
            "part": "Brake Pads",
            "quantity": 50,
            "price": 100.00
        }
        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part'], "Brake Pads")

    def test_invalid_creation(self):
        inventory_payload = {
            "part": "Brake Pads",
            "quantity": 50
        }
        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    def test_update_inventory_item(self):
        inventory_payload = {
            "part": "Brake Pads",
            "quantity": 50,
            "price": 100.00
        }
        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)

        update_payload = {
            "part": "Brake Pads",
            "quantity": 60,
            "price": 120.00
        }
        response = self.client.put(f'/inventory/{response.json["id"]}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['quantity'], 60)
        self.assertEqual(response.json['price'], 120.00)

    def test_delete_inventory_item(self):
        inventory_payload = {
            "part": "Brake Pads",
            "quantity": 50,
            "price": 100.00
        }
        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(f'/inventory/{response.json["id"]}')
        self.assertEqual(response.status_code, 200)