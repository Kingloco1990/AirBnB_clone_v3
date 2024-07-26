#!/usr/bin/python3
"""
Flask Application Setup

This module sets up and configures a Flask application with the following
features:
- Registers a Flask blueprint (`app_views`) for API routes.
- Configures Cross-Origin Resource Sharing (CORS) to allow requests
  from all origins.
- Defines a teardown function to close the database storage when the
  application context ends.
- Provides a custom error handler for 404 errors, returning a
  JSON response with an error message.
- Reads the host and port for the application from environment variables,
  defaulting to '0.0.0.0' and '5000', respectively.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

# Create a CORS instance allowing all origins
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Close the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
