#!/usr/bin/python3
"""A new view for Place obs that handles all default RESTFul API."""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Place objects associated with city_id"""
    dict_n = []
    objs = storage.all(Place).values()
    for o in objs:
        if o.to_dict()['city_id'] == city_id:
            dict_n.append(o.to_dict())
    if len(dict_n) != 0:
        return (jsonify(dict_n))
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def pl_id(place_id):
    """Retrieves a Place object with the specified id, otherwise 404"""
    obj = storage.get(Place, place_id)
    if obj is not None:
        return (jsonify(obj.to_dict()))
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def pl_del(place_id):
    """Deletes a Place object"""
    obj = storage.get(Place, place_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def pl_post():
    """Creates a Place"""
    data = request.get_json()
    obj = storage.get(City, city_id)
    usr_o = storage.get(User, data.get('user_id'))
    if obj is None or usr_o is None:
        abort(404)
    elif not data:
         abort(400, 'Not a JSON')
    elif 'user_id' not in data:
         abort(400, 'Missing user_id')
    elif 'name' not in data:
         abort(400, 'Missing name')
    pl = Place()
    pl.name = data.get('name')
    pl.user_id = data.get('user_id')
    storage.new(pl)
    storage.save()
    return jsonify(pl.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def pl_update(state_id):
    """Updates a Place object"""
    obj = storage.get(Place, place_id)
    if obj is not None:
        data = request.get_json()
        if not data:
             abort(400, 'Not a JSON')
        for k in data.keys():
            if k == 'id' or k == 'created_at' or k == 'updated_at'\
            or k == 'user_id' or k == 'city_id':
                pass
            else:
                obj.name = data.get(k)
        storage.save()
        return jsonify(obj.to_dict()), 200
    abort(404)
