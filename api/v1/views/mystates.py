#!/usr/bin/python3
"""A new view that handles all default RESTFul API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    dict_n = []
    objs = storage.all(State).values()
    for o in objs:
        dict_n.append(o.to_dict())
    return (jsonify(dict_n))


@app_views.route('/states/<state_id>', methods=['GET'])
def st_id(state_id):
    """Retrieves a State object with the specified id, otherwise 404"""
    obj = storage.get(State, state_id)
    if obj is not None:
        return (jsonify(obj.to_dict()))
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """Creates a State"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif 'name' not in data:
        abort(400, 'Missing name')
    st = State()
    st.name = data.get('name')
    storage.new(st)
    storage.save()
    return jsonify(st.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    if obj is not None:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k in data.keys():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                pass
            else:
                obj.name = data.get(k)
        storage.save()
        return jsonify(obj.to_dict()), 200
    abort(404)
