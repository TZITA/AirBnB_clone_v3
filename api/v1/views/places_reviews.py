#!/usr/bin/python3
"""A new view that handles all default RESTFul API actions"""
from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews(place_id):
    """Retrieves the list of all Review objects"""
    dict_n = []
    objs = storage.all(Review).values()
    for o in objs:
        if o.to_dict()['place_id'] == place_id:
            dict_n.append(o.to_dict())
    return (jsonify(dict_n))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def rev_id(review_id):
    """Retrieves a Review object with the specified id, otherwise 404"""
    obj = storage.get(Review, review_id)
    if obj is not None:
        return (jsonify(obj.to_dict()))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_del(review_id):
    """Deletes a Review object"""
    obj = storage.get(Review, review_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def rev_post():
    """Creates a Review"""
    data = request.get_json()
    pl_o = storage.get(Place, place_id)
    usr_o = storage.get(User, data.get('user_id'))
    if pl_o is None or usr_o is None:
        abort(404)
    elif not data:
        abort(400, 'Not a JSON')
    elif 'text' not in data:
        abort(400, 'Missing text')
    elif 'user_id' not in data:
        abort(400, 'Missing user_id')
    rev = Review()
    rev.text = data.get('text')
    rev.user_id = data.get('user_id')
    storage.new(rev)
    storage.save()
    return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def rev_update(state_id):
    """Updates a Review object"""
    obj = storage.get(Review, review_id)
    if obj is not None:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k in data.keys():
            if k == 'id' or k == 'created_at' or k == 'updated_at'\
               or k == 'place_id' or k == 'user_id':
                pass
            elif k == 'text':
                obj.text = data.get(k)
        storage.save()
        return jsonify(obj.to_dict()), 200
    abort(404)
