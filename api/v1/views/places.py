#!/usr/bin/python3

""" Handles all restful API actions for Place"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def pl_1(place_id):
    """Retrives, deletes, updates a place object"""
    pl_obj = storage.get(Place, place_id)
    if pl_obj is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(pl_obj)
    if request.method == 'DELETE':
        pl_obj.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()

        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            setattr(pl_obj, k, v)
            pl_obj.save()
            return jsonify(pl_obj.to_dict), 200

@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def pl_2(city_id):
    """Retrives and creates place objects"""
    p_obs = storage.all(Place)
    pls = [o.to_dict() for o in p_obs.values() if o['city_id'] == city_id]
    if len(places):
        abort(404)

    if request.method == 'GET':
        return jsonify(places)
    if request.method == 'POST':
        data = request.get_json()

        if data is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' not in data:
            abort(400, 'Missing name')
        u = storage.all(User)
        users = [o.to_dict() for o in u.values() if o['id'] == data['user_id']]
        if len(users) == 0:
            abort(404)
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
