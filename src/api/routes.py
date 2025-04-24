"""
This module takes care of starting the API Server, loading the DB,
and adding the endpoints including authentication.
"""
from flask import request, jsonify, Blueprint
from flask_cors import CORS
from api.models import db, User, PackingItem
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)
CORS(api)

@api.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello from the backend!"}), 200

@api.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"msg": "User already exists"}), 400

    user = User(email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 200

@api.route('/token', methods=['POST'])
def create_token():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200

@api.route('/PackingList', methods=['GET'])
@jwt_required()
def private():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"msg": f"Welcome, {user.email}!"}), 200



# Get all packing items for current user
@api.route('/packing-items', methods=['GET'])
@jwt_required()
def get_packing_items():
    user_id = get_jwt_identity()
    items = PackingItem.query.filter_by(user_id=user_id).all()
    return jsonify([item.serialize() for item in items]), 200

# Add a new packing item
@api.route('/packing-items', methods=['POST'])
@jwt_required()
def add_packing_item():
    user_id = get_jwt_identity()
    content = request.json.get("content")
    if not content:
        return jsonify({"msg": "Content is required"}), 400
    item = PackingItem(user_id=user_id, content=content)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201

# Delete an item
@api.route('/packing-items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_packing_item(item_id):
    user_id = get_jwt_identity()
    item = PackingItem.query.get(item_id)
    if item is None or item.user_id != user_id:
        return jsonify({"msg": "Item not found or unauthorized"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"msg": "Item deleted"}), 200
