#!/usr/bin/python3
"""app_views route /status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a JSON: status: OK"""
    stat = {
            "status": "OK"
        }
    return (jsonify(stat))
