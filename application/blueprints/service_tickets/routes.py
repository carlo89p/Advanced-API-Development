from flask import request, jsonify
from . import service_tickets_bp
from extensions import db
from .schemas import service_ticket_schema, service_tickets_schema
from models import ServiceTicket, Mechanic, MechanicService, Inventory
from marshmallow import ValidationError
from sqlalchemy import select

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = ServiceTicket(**service_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    service_tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(service_tickets)

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({"error": "Service ticket not found."}), 404

@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 404
    
    mechanic_service = MechanicService(ticket_id=ticket_id, mechanic_id=mechanic_id)
    db.session.add(mechanic_service)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 404
    
    assignment = db.session.execute(
        select(MechanicService).where(
            MechanicService.ticket_id == ticket_id,
            MechanicService.mechanic_id == mechanic_id
        )
    ).scalar_one_or_none()

    if not assignment:
        return jsonify({"error": "Assignment not found."}), 404

    db.session.delete(assignment)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_mechanics(ticket_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    data = request.json
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic:
            new_assignment = MechanicService(ticket_id=ticket_id, mechanic_id=mechanic_id)
            db.session.add(new_assignment)

    for mechanic_id in remove_ids:
        assignment = db.session.execute(
            select(MechanicService).where(
                MechanicService.ticket_id == ticket_id,
                MechanicService.mechanic_id == mechanic_id
            )
        ).scalar_one_or_none()
        if assignment:
            db.session.delete(assignment)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    inventory_item = db.session.get(Inventory, inventory_id)
    if not inventory_item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    service_ticket.inventory.append(inventory_item)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200