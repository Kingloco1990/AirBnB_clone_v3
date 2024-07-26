#!/usr/bin/python3
"""
API Index Routes

This module defines the index routes for the API, including:
- `/status`: Returns the status of the API with a JSON response
  indicating "OK".
- `/stats`: Retrieves and returns the number of objects of each type
  (Amenity, City, Place, Review, State, User) in the database.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
