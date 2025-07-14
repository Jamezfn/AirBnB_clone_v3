#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort, request, jsonify, Response
from models import storage
from models.user import User
import json

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_user():
    """Retrieve all users"""
    users = storage.all(User)
    return Response(json.dumps([user.to_dict() for user in users.values()], indent=4), mimetype='application/json')

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve user with user id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return Response(json.dumps(user.to_dict(), indent=4), mimetype='appliction/json')

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete user with user id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return Response(json.dumps(new_user.to_dict(), indent=4), status=201, mimetype='application/json')

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update user details with user id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key in ("id", "email", "created_at", "updated_at"):
            continue
        setattr(user, key, value)
    storage.save()
    return Response(json.dumps(user.to_dict(), indent=4), status=200, mimetype='application/json')
