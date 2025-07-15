#!/usr/bin/python3
from api.v1.views import app_views
from flask import abort, request, jsonify, Response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
import json

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    """Retrieve a list of all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews if hasattr(place, 'reviews') else []
    return Response(json.dumps([review.to_dict() for review in reviews], indent=4), mimetype='application/json')

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve review with review id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return Response(json.dumps(review.to_dict(), indent=4), mimetype='application/json')

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review with id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jasonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a review of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, description='Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return Response(json.dumps(new_review.to_dict(), indent=4), status=201, mimetype='application/json')

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update review with review id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key in ("id", "user_id", "place_id", "created_at", "updated_at"):
            continue
        if hasattr(review, key):
            setattr(review, key, value)
    storage.save()
    return Response(json.dumps(review.to_dict(), indent=4), status=200, mimetype='application/json')
