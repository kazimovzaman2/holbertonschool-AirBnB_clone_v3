#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
    "/amenities",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def amenity():
    """
    Retrieves the list of amenities
    """
    if request.method == "GET":
        amenities = storage.all(Amenity).values()
        amenities_list = []
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    elif request.method == "POST":
        request_body = request.get_json(silent=True)
        if not request_body:
            abort(400, "Not a JSON")
        elif "name" not in request_body:
            abort(400, "Missing name")
        new_amenity = Amenity(**request_body)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def get_amenity(amenity_id):
    """Returns an object by id"""
    if request.method == "GET":
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        request_body = request.get_json(silent=True)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")
        for key, value in request_body.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
