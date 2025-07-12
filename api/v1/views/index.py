from api.v1.views import app_views
from flask import jsonify, Response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return JSON status OK"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number od each object by type"""
    return Response(json.dumps({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        },
                    indent=4,), mimetype='application/json')
