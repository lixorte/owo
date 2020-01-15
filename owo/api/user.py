from pymongo import MongoClient
from loguru import logger
from flask import Blueprint, request, jsonify
from owo.api.utils import schema_validator
import owo.api.schemas as schemas
from flask_jwt_extended import jwt_required


client = MongoClient('mongodb://mongo:27017/', connect=False)
user = Blueprint('users', __name__)


@user.route("/user", methods=["get"])
@schema_validator(schemas.get_users)
def get_users():
    data = request.get_json()

    offset = data.get("offset", None) or 0
    limit = data.get("limit")
    utype = data.get("type")

    out = list()

    for idx, item in enumerate(
        client["meta"]["users"].find().sort("login")
    ):
        if idx < offset:
            continue
        if idx > offset + limit:
            break
        if ((utype == "admin" and data["state"] != "admin")
                or (utype == "normal" and data["state"] != "normal")):
            continue
        else:
            del item["ejtoken"]
            item["id"] = str(item["_id"])
            del item["_id"]

            out.append(item)

    return (jsonify(out), 200)


@user.route("/user/{string:user_id}", methods=["GET"])
@jwt_required
def get_user(user_id):
    user = client["meta"]["users"].find_one({"name": user_id})

    if user is None:
        return ({
            "message": "No such user",
            "code": 404
        }, 404)

    del user["_id"]

    return (jsonify(user), 200)  # TODO Test with JWT


@user.route("/user/{string:user_id}", methods=["POST"])
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
