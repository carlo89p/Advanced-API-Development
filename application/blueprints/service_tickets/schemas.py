from extensions import db, ma
from models import ServiceTicket, Mechanic
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
    
    mechanics = fields.List(fields.Nested(MechanicSchema))

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)