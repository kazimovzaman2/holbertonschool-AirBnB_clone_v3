#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def review_by_place(place_id):
    """
    Retrieves the list of review by place
    """
    if request.method == "GET":
        review_list = []
        place_obj = storage.get(Place, place_id)

        if place_obj is None:
            abort(404)
        for obj in place_obj.reviews:
            review_list.append(obj.to_dict())

        return jsonify(review_list)
    elif request.method == "POST":
        request_body = request.get_json(silent=True)

        if not request_body:
            abort(400, "Not a JSON")
        elif "text" not in request_body:
            abort(400, "Missing text")
        elif "user_id" not in request_body:
            abort(400, "Missing user_id")

        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)

        user = storage.get(User, request_body["user_id"])
        if user is None:
            abort(404)

        new_review = Review(**request_body)
        new_review.place_id = place_id
        new_review.save()

        return jsonify(new_review.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def reviews(review_id):
    """ """
    if request.method == "GET":
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        storage.delete(review)
        storage.save()

        return jsonify({}), 200
    elif request.method == "PUT":
        request_body = request.get_json(silent=True)
        review_obj = storage.get(Review, review_id)

        if review_obj is None:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")

        for key, value in request_body.items():
            if key not in [
                "id", "user_id", "place_id", "created_at", "updated_at"
            ]:
                setattr(review_obj, key, value)
        storage.save()

        return jsonify(review_obj.to_dict()), 200
