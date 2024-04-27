#!/usr/bin/python3
"""Module for the API"""
from os import getenv
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    "/places/<place_id>/amenities",
    methods=["GET"],
    strict_slashes=False,
)
def get_place_amenities(place_id):
    """
    Retrieves the list of amenities by place
    """
    amenity_list = []
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)
    for obj in place_obj.amenities:
        amenity_list.append(obj.to_dict())

    return jsonify(amenity_list)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE", "POST"],
    strict_slashes=False,
)
def link_place_amenity(place_id, amenity_id):
    """
    Deletes an amenity by place
    """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not place_obj or not amenity_obj:
        abort(404)

    if request.method == "DELETE":
        found_amenity = None

        for obj in place_obj.amenities:
            if str(obj.id) == amenity_id:
                if getenv("HBNB_TYPE_STORAGE") == "db":
                    place_obj.amenities.remove(obj)
                else:
                    place_obj.amenity_ids.remove(obj.id)
                place_obj.save()
                found_amenity = obj
                break

        if found_amenity is None:
            abort(404)
        else:
            return jsonify({}), 201

    elif request.method == "POST":
        found_amenity = None

        for obj in place_obj.amenities:
            if str(obj.id) == amenity_id:
                found_amenity = obj
                break

        if found_amenity:
            return jsonify(found_amenity.to_json())

        if getenv("HBNB_TYPE_STORAGE") == "db":
            place_obj.amenities.append(amenity_obj)
        else:
            place_obj.amenities = amenity_obj

        place_obj.save()

        resp = jsonify(amenity_obj.to_json())
        resp.status_code = 201
        return resp
