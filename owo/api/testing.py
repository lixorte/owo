from pymongo import MongoClient
from loguru import logger
from .utils import prefs_validator
import uuid
from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies


client = MongoClient('mongodb://mongo:27017/', connect=False)

tesing_blueprint = Blueprint('testing', __name__)


@tesing_blueprint.route("/testing/get_jwt")
@jwt_required
def get_jwt():
    return get_jwt_identity()


@tesing_blueprint.route("/only/admin")
@jwt_required
@prefs_validator({"type": "admin"})
def only_admin():
    return "Hello admin"


@tesing_blueprint.route("/only/banned")
@jwt_required
@prefs_validator({"state": "banned"})
def only_banned():
    return "Hello looser"


@tesing_blueprint.route("/new/admin")
def create_admin():
    user = {
        "name": uuid.uuid4().hex,  # id
        "title": "TEST ADMIN",  # RL name
        "type": "ok",
        "state": "admin"
        }

    client["meta"]["users"].insert_one(user)

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    resp = make_response("OK")

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


@tesing_blueprint.route("/new/user")
def create_user():
    user = {
        "name": uuid.uuid4().hex,  # id
        "title": "TEST USER",  # RL name
        "type": "ok",
        "state": "normal"
        }

    client["meta"]["users"].insert_one(user)

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    resp = make_response("OK")

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


@tesing_blueprint.route("/drop/db")
def drop_db():
    for db in client.list_databases():
        if db["name"] not in ["admin", "config", "local"]:
            client.drop_database(db['name'])

    return "OK"
