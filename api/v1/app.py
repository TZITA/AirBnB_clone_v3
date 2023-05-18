#!/usr/bin/python3

""" Flask instance and registering Blueprint."""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Returns custom 404 error."""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close(exception):
    """Calls storage.close()."""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
