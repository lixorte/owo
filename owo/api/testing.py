from pymongo import MongoClient
from loguru import logger
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity


client = MongoClient('mongodb://mongo:27017/', connect=False)

tesing_blueprint = Blueprint('testing', __name__)


@tesing_blueprint.route("/testing/get_jwt")
@jwt_required
def get_jwt():
    return get_jwt_identity()
