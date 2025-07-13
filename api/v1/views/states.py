from flask import jsonify, Response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
import json

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return list of all State objects"""
    states = storage.all(State).values()
    return Response(json.dumps([state.to_dict() for state in states], indent=4), mimetype='application/json')

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return one State by ID, or 404 if not found"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return Response(json.dumps(state.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State from posted JSON"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return Response(json.dumps(new_state.to_dict(), indent=4), mimetype='application/json'), 201

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a State by ID, or 404 if not found"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update an existing State by ID, or 404 if not found"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignore = {'id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return Response(json.dumps(state.to_dict(), indent=4), status=200, mimetype='application/json')
