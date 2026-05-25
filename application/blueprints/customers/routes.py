from flask import request, jsonify
from . import customers_bp
from extensions import db, limiter
from .schemas import customer_schema, customers_schema, login_schema
from models import Customer, ServiceTicket
from marshmallow import ValidationError
from sqlalchemy import select
from extensions import cache
from application.utils.util import encode_token, token_required

@customers_bp.route('/', methods=['POST'])
@limiter.limit("20 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    query = select(Customer).limit(page_size).offset((page - 1) * page_size)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers)

@customers_bp.route('/<int:customer_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer {customer_id} successfully deleted.'}), 200

@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == credentials['email'])
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == credentials['password']:
        auth_token = encode_token(customer.id)
        return jsonify({"status": "success", "message": "Successfully Logged In", "auth_token": auth_token}), 200
    return jsonify({'message': "Invalid email or password"}), 401
    
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    from application.blueprints.service_tickets.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(tickets), 200

@customers_bp.route('/me', methods=['DELETE'])
@token_required
def delete_my_account(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted user {customer_id}"})