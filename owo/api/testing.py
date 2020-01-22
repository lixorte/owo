from pymongo import MongoClient
from loguru import logger
from .utils import prefs_validator
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity


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
