from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import Response, abort, request, jsonify
import json

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """List all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities if hasattr(state, 'cities') else []
    return Response(json.dumps([city.to_dict() for city in cities], indent=4), mimetype='application/json')

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a single City by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return Response(json.dumps(city.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City under a given State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return Response(json.dumps(new_city.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Delete a City by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update an existing City by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, val in data.items():
        if key in ('id', 'state_id', 'created_at', 'updated_at'):
            continue
        setattr(city, key, val)
    storage.save()
    return Response(json.dumps(city.to_dict(), indent=4), status=200, mimetype='applictation/json')
