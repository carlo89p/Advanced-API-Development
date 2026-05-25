from flask import request, jsonify
from . import inventory_bp
from extensions import db, limiter, cache
from .schemas import inventory_schema, inventories_schema
from models import Inventory
from marshmallow import ValidationError
from sqlalchemy import select

@inventory_bp.route('/', methods=['POST'])
@limiter.limit("200 per day")
def create_inventory_item():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_item = Inventory(**inventory_data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201

@inventory_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_inventory():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    query = select(Inventory).limit(page_size).offset((page - 1) * page_size)
    items = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(items), 200

@inventory_bp.route('/<int:item_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if item:
        return inventory_schema.jsonify(item), 200
    return jsonify({"error": "Inventory item not found."}), 404

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in inventory_data.items():
        setattr(item, key, value)
    db.session.commit()
    return inventory_schema.jsonify(item), 200

@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Inventory item {item_id} successfully deleted."}), 200