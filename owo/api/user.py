from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

client = MongoClient('mongodb://mongo:27017/', connect=False)
user = Blueprint('users', __name__)


@user.route("/", methods=["GET"])
def get_users():
    out = []

    for user in client["meta"]["users"].find().sort("login"):
        out.append(user)

    return jsonify(out)


@user.route("/{string:user_id}", methods=["GET"])
@jwt_required
def get_user(user_id):
    user = client["meta"]["users"].find_one({"name": user_id})

    if user is None:
        return ({
                    "message": "No such user",
                    "code": 404
                }, 404)

    del user["_id"]

    return jsonify(user), 200  # TODO Test with JWT


@user.route("/{string:user_id}", methods=["POST"])
@jwt_required
def edit_user(user_id):
    data = request.get_json()
    user = client["meta"]["users"].find_one({"name": user_id})

    if user is None:
        return ({
                    "message": "No such user",
                    "code": 404
                }, 404)

    user_type = data["type"] or user["type"]
    state = data["state"] or user["state"]

    client["meta"]["users"].update_one(
        {"name": user_id}, {"type": user_type, "state": state})

    user["type"] = user_type
    user["state"] = state

    del user["_id"]

    return jsonify(user), 200  # TODO Test with JWT
