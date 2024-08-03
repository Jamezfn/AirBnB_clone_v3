#!/usr/bin/python3
"""
Return status of the page
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Retrieve response status.
    This fx is associated with the /status endpoint
    and responds with a JSON object indicating that the API
    is running
    """
    return jsonify({
        'status': 'OK'
    })

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieve the number of each object by type.
    This fx is associated with the /sta
    """
    try:
        return jsonify({
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
