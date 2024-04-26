#!/usr/bin/python3
"""Module for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states():
    """Return states"""
    if request.method == "GET":
        states = storage.all(State).values()
        states_list = []
        for state in states:
            states_list.append(state.to_dict())
        return jsonify(states_list)
    elif request.method == "POST":
        state_data = request.get_json(silent=True)
        if not state_data:
            abort(400, "Not a JSON")
        elif "name" not in state_data:
            abort(400, "Missing name")
        new_state = State(**state_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
    "/states/<state_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def get_state(state_id):
    """Returns an object by id"""
    if request.method == "GET":
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        state_data = request.get_json(silent=True)
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        elif not state_data:
            abort(400, "Not a JSON")
        for key, value in state_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
