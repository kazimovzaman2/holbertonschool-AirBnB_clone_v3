#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/cities", methods=["GET", "POST"], strict_slashes=False)
def cities():
    """Return cities"""
    if request.method == "GET":
        cities = storage.all(City).values()
        cities_list = []
        for city in cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    elif request.method == "POST":
        city_data = request.get_json(silent=True)
        if not city_data:
            abort(400, "Not a JSON")
        elif "name" not in city_data:
            abort(400, "Missing name")
        new_city = City(**city_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
    "/cities/<city_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def get_city(city_id):
    """Returns an object by id"""
    if request.method == "GET":
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        city_data = request.get_json(silent=True)
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        elif not city_data:
            abort(400, "Not a JSON")
        for key, value in city_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False,
)
def city_by_state(state_id):
    """
    Retrieves the list of cities by state
    """
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)
