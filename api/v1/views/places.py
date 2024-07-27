#!/usr/bin/python3
"""
Defines RESTful API endpoints for managing Place objects.
"""
import os
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieve Place objects based on search criteria"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        # Retrieve all Place objects
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = set()

    # Retrieve Place objects based on states
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)

    # Retrieve Place objects based on cities
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    # Filter Place objects based on amenities
    if amenities:
        places = [
            place for place in places
            if all(amenity.id in place.amenity_ids
                   for amenity in amenities)]

    return jsonify([place.to_dict() for place in places])
