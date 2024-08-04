#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from models.state import State
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    Handles GET /api/v1/states
    """
    all_states = storage.all(State)
    all_states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a specific state object.
    Handles GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.
    Handles DELETE /api/vi/state/<state_id>
    """
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        storage.save()
    except Exception:
        abort(404, description= 'Not found')
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def post_state(state_id):
    """
    Creates a new state
    Handles POST /api/v1/states
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    instance = State(**data)
    storage.new(instance)
    storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Update an existing State object.
    Handles PUT /api/v1/states/<state_id>
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    ignore = ['id', 'created_at', 'update_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
