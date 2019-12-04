from pymongo import MongoClient
from loguru import logger
from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required
from owo.api.utils import schema_validator
from owo.api.schemas import *


logger.add("api_election.log", colorize=True,
           format="<green>{time}</green> <level>{message}</level>",
           rotation="1 day", backtrace=True, diagnose=True)

client = MongoClient('mongodb://mongo:27017/', connect=False)
election = Blueprint('elections', __name__)


@election.route("/election/new", methods=["POST"])  # TODO Test
@jwt_required
@schema_validator(create_election)
def new_election():
    data = request.get_json()

    name = data["name"]
    state = data["state"]
    el_type = data["type"]

    new_el = {
        "name": name,
        "type": el_type,
        "state": state,
        "datetime": datetime.now()
    }

    new_id = str(client["elections"]["meta"].insert_one(new_el))
    new_el["id"] = new_id

    client["elections"].create_collection(new_id)

    return jsonify(new_el), 200
