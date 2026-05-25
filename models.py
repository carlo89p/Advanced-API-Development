from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from typing import List

ticket_inventory = db.Table(
    'ticket_inventory',
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.ForeignKey('inventory.id'), primary_key=True)
)

# mechanic_service = db.Table(
#     'mechanic_service',
#     db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
#     db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
# )

class MechanicService(db.Model):
    __tablename__ = 'mechanic_service'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), nullable=False)
    date_started: Mapped[date] = mapped_column(nullable=True)
    time_started: Mapped[date] = mapped_column(nullable=True)
    date_completed: Mapped[date] = mapped_column(nullable=True)
    time_completed: Mapped[date] = mapped_column(nullable=True)

    mechanic: Mapped['Mechanic'] = db.relationship(back_populates='mechanic_services')
    service_ticket: Mapped['ServiceTicket'] = db.relationship(back_populates='mechanic_services')

class Customer(db.Model):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    DOB: Mapped[date]
    address: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    position: Mapped[str] = mapped_column(db.String(200), nullable=False)


    mechanic_services: Mapped[List['MechanicService']] = db.relationship(back_populates='mechanic')

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_date: Mapped[date]
    days_required: Mapped[int] = mapped_column(nullable=False)
    issue_reported: Mapped[str] = mapped_column(db.Text, nullable=False)
    jobs_done: Mapped[str] = mapped_column(db.Text, nullable=False)
    pickup_dropoff: Mapped[bool] = mapped_column(nullable=False)
    followup_reqd: Mapped[bool] = mapped_column(nullable=False)
    job_completed: Mapped[bool] = mapped_column(nullable=False)

    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanic_services: Mapped[List['MechanicService']] = db.relationship(back_populates='service_ticket')
    inventory: Mapped[List['Inventory']] = db.relationship(secondary=ticket_inventory, back_populates='service_tickets')

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    part: Mapped[str] = mapped_column(db.String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=ticket_inventory, back_populates='inventory')

