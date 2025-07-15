from api.v1.views import app_views
from flask import abort, request, jsonify, Response 
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def List_places(city_id):
    """Retrieve all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places if hasattr(city, 'places') else []
    return Response(json.dumps([place.to_dict() for place in places], indent=4), mimetype='application/json')

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve place with place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return Response(json.dumps(place.to_dict(), indent=4), mimetype='appliction/json')

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete place with place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a new place in city with city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return Response(json.dumps(new_place.to_dict(), indent=4), status=201, mimetype='application/json')

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update place with place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ("id", "user_id", "city_id", "created_at", "updated_at"):
            if hasattr(place, key):
                setattr(place, key, value)
    storage.save()
    return Response(json.dumps(place.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/places/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """Search Places by states, cities, and amenities"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    state_ids = data.get('states', [])
    city_ids = data.get('cities', [])
    amenity_ids = data.get('amenities', [])

    places_set = set()

    for st_id in state_ids:
        state = storage.get(State, st_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    places_set.add(place)

    for ct_id in city_ids:
        city = storage.get(City, ct_id)
        if city:
            for place in city.places:
                places_set.add(place)

    if not state_ids and not city_ids:
        for place in storage.all(Place).values():
            places_set.add(place)
    if amenity_ids:
        filtered = set()
        for place in places_set:
            ok = True
            for am_id in amenity_ids:
                amenity = storage.get(Amenity, am_id)
                if not amenity:
                    ok = False
                    break
                if hasattr(place, 'amenities'):
                    if amenity not in place.amenities:
                        ok = False
                        break
                else:
                    if am_id not in place.amenity_ids:
                        ok = False
                        break
            if ok:
                filtered.add(place)
        places_set = filtered

    result = [place.to_dict() for place in places_set]
    return jsonify(result)
