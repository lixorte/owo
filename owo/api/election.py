from pymongo import MongoClient
from bson import ObjectId
from loguru import logger
from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from owo.api.utils import schema_validator, fetch_eleciton
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

    client["elections"].create_collection("banned"+new_id)
    client["elections"].create_collection("voted"+new_id)
    client["elections"].create_collection("normal"+new_id)

    logger.info(f"Created ellection with name {name}")

    return jsonify(new_el), 200


@election.route("/election/{string:election_id}", methods=["GET"])
@schema_validator(get_election_info)
def get_el_info(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info("Get request to unknown election " + election_id)
        return 404

    return jsonify(fetch_eleciton(election_id)), 200  # TODO Test


@election.route("/election/{string:election_id}", methods=["PATCH"])
@jwt_required
@schema_validator(update_election_info)
def patch_el_info(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info("Patch request to unknown election " + election_id)
        return 404

    client["elections"]["meta"].find_one_and_update(
        {"_id": ObjectId(election_id)},
        {"$set": request.get_json()}
    )

    return 200


@election.route("/election/{string:election_id}", methods=["DELETE"])
@jwt_required
@schema_validator(delete_election)
def del_election(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info("Delete request to unknown election " + election_id)
        return 404

    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    client["elections"]["meta"].delete_one({"_id": ObjectId(election_id)})

    client["elections"]["banned"+election_id].drop()
    client["elections"]["voted"+election_id].drop()
    client["elections"]["normal"+election_id].drop()

    logger.info(
        f"Election {election_id} with name {election['name']} was deleted")

    return 200


@election.route("/election/{string:election_id}/vote/new", methods=["POST"])
@jwt_required
@schema_validator(add_option)
def add_opt(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info("Add vote request to unknown election " + election_id)
        return 404

    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    data = request.get_json()

    if data["type"] != election["type"]:
        logger.info("Wrong vote type on new vote")
        return 400

    if data["type"] == "topic":
        new_vote = {
            "name": data["name"],
            "voters": [get_jwt_identity()["name"]],
            "userAdded": get_jwt_identity()["name"]
        }

    else:
        new_vote = {
            "name": data["name"],
            "voters": [get_jwt_identity()["name"]],
            "userAdded": get_jwt_identity()["name"],
            "serviceLink": data["serviceLink"],
            "cutCommentary": data["cutCommentary"],
            "album": data["album"],
            "singer": data["singer"]
        }

    new_id = client["elections"]["normal"+election_id].insert_one(new_vote)

    new_vote["id"] = str(new_id)

    return jsonify(new_vote), 200  # TODO Test
