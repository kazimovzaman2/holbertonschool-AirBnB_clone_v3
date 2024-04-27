#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def place_by_city(city_id):
    """
    Retrieves the list of place by city
    """
    if request.method == "GET":
        place_list = []
        city_obj = storage.get(City, city_id)

        if city_obj is None:
            abort(404)
        for obj in city_obj.cities:
            place_list.append(obj.to_dict())

        return jsonify(place_list)
    elif request.method == "POST":
        request_body = request.get_json(silent=True)
        city_obj = storage.get(City, city_id)

        if city_obj is None:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")
        elif "name" not in request_body:
            abort(400, "Missing name")
        elif "user_id" not in request_body:
            abort(400, "Missing user_id")

        user = storage.get(User, request_body["user_id"])
        if user is None:
            abort(404)

        request_body["city_id"] = city_id
        new_place = Place(**request_body)
        new_place.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def places(place_id):
    """ """
    if request.method == "GET":
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        storage.delete(place)
        storage.save()

        return jsonify({}), 200
    elif request.method == "PUT":
        request_body = request.get_json(silent=True)
        place_obj = storage.get(Place, place_id)

        if place_obj is None:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")

        for key, value in request_body.items():
            if key not in [
                "id", "user_id", "city_id", "created_at", "updated_at"
            ]:
                setattr(place_obj, key, value)
        storage.save()

        return jsonify(place_obj.to_dict()), 200
