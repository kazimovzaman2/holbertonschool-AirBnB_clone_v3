#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def city_by_state(state_id):
    """
    Retrieves the list of cities by state
    """
    if request.method == "GET":
        city_list = []
        state_obj = storage.get(State, state_id)

        if state_obj is None:
            abort(404)
        for obj in state_obj.cities:
            city_list.append(obj.to_dict())

        return jsonify(city_list)
    elif request.method == "POST":
        request_body = request.get_json(silent=True)
        state_obj = storage.get(State, state_id)

        if state_obj is None:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")
        elif "name" not in request_body:
            abort(400, "Missing name")

        new_city = State(**request_body)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
    "/cities/<city_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def cities(city_id):
    """ """
    if request.method == "GET":
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        storage.delete(city)
        storage.save()

        return jsonify({}), 200
    elif request.method == "PUT":
        request_body = request.get_json(silent=True)
        city_obj = storage.get(City, city_id)

        if city_obj is None:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")

        for key, value in request_body.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(request_body, key, value)
        storage.save()

        return jsonify(city_obj.to_dict()), 200
