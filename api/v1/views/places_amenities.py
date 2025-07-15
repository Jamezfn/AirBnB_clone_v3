from api.v1.views import app_views
from flask import abort, request, jsonify, Response
from models import storage
from models.amenity import Amenity
from models.place import Place
import json

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def list_place_amenities(place_id):
    """Retrieve amenities of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_amenities = []
    if hasattr(place, 'amenities'):
        list_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                list_amenities.append(amenity.to_dict())
    return Response(json.dumps(list_amenities, indent=4), mimetype='appliction/json')

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete(place_id, amenity_id):
    """Delete an Amenity from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if hasattr(place, 'amenities'):
        if amenity in place.amenities:
            place.amenities.remove(amenity)
    else:
        if amenity_id in place.amenity_ids:
            place.amenities_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def create_place_amenity(amenity_id, place_id):
    """Link an Amenity to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if hasattr(place, 'amenities'):
        if amenity in place.amenities:
            return Response(json.dumps(amenity.to_dict(), indent=4), status=200,
                            mimetype='application/json')
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
             return Response(json.dumps(amenity.to_dict(), indent=4), status=200,
                             mimetype='application/json')
        place.amenity_id.append(amenity)
    storage.save()
    return Response(json.dumps(amenity.to_dict(), indent=4), status=200,
                             mimetype='application/json')
