#!/usr/bin/python3
"""Module for the API"""
from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Return stats"""

    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users",
    }
    return jsonify({key: storage.count(value) for key, value in classes.items()})
