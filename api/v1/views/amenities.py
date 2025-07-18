from flask import jsonify, Response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve all the amenities"""
    amenities = storage.all(Amenity)
    return Response(json.dumps([amenity.to_dict() for amenity in amenities.values()], indent=4), mimetype='application/json')

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve amenity with amenity id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return Response(json.dumps(amenity.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete amenity with amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, descriptio='Missing name')
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return Response(json.dumps(new_amenity.to_dict(), indent=4), status=201, mimetype='appliction/json')

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity with amenity id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key in ("id", "created_at", "updated_at"):
            continue
        setattr(amenity, key, value)
    storage.save()
    return Response(json.dumps(amenity.to_dict(), indent=4), status=200, mimetype='application/json')
