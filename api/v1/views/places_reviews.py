#!/usr/bin/python3

"""A new view that handles all default RESTFul API actions"""

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews(place_id):
    """Retrieves the list of all Review objects or creates a review object"""
    rev = storage.all(Review).values()
    revs = [o.to_dict() for o in rev if o.to_dict()['place_id'] == place_id]
    pl_o = storage.get(Place, place_id)
    if pl_o is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(revs)
    if request.method == 'POST':
        data = request.get_json()

        usr_o = storage.get(User, data.get('user_id'))
        if usr_o is None:
            abort(404)
        if not data:
            abort(400, 'Not a JSON')
        if data.get('text') is None:
            abort(400, 'Missing text')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')

        new_rev = Review(**data)
        new_rev.save()
        return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def rev_id(review_id):
    """Retrieves, deletes and updates a Review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(rev.to_dict())
    if request.method == 'DELETE':
        rev.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            setattr(rev, k, v)
        rev.save()
        return jsonify(rev.to_dict()), 200
