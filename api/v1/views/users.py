#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    "/users",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def user():
    """
    Retrieves the list of users
    """
    if request.method == "GET":
        users = storage.all(User).values()
        user_list = []
        for user in users:
            user_list.append(user.to_dict())
        return jsonify(user_list)
    elif request.method == "POST":
        request_body = request.get_json(silent=True)
        if not request_body:
            abort(400, "Not a JSON")
        elif "name" not in request_body:
            abort(400, "Missing name")
        new_user = User(**request_body)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route(
    "/users/<user_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def get_user(user_id):
    """Returns an object by id"""
    if request.method == "GET":
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        request_body = request.get_json(silent=True)
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        elif not request_body:
            abort(400, "Not a JSON")
        for key, value in request_body.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
