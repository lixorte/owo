from pymongo import MongoClient
from bson import ObjectId
from loguru import logger
from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from owo.api.utils import schema_validator, fetch_election, normalize_id, fetch_election_by_meta
from owo.api.schemas import *

client = MongoClient('mongodb://mongo:27017/', connect=False)
election_blueprint = Blueprint('elections', __name__)


@election_blueprint.route("/<string:election_id>", methods=["GET"])
def get_el_info(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info(f"Get request to unknown election {election_id}")
        return "Error", 404

    return jsonify(fetch_election(election_id)), 200  # TODO Test


@election_blueprint.route("/new", methods=["POST"])  # TODO Test
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

    new_id = str(client["elections"]["meta"].insert_one(new_el).inserted_id)
    new_el["id"] = new_id

    client["elections"].create_collection("banned" + new_id)
    client["elections"].create_collection("voted" + new_id)  # Ones which won
    client["elections"].create_collection("normal" + new_id)

    logger.info(f"Created election with name {name}")

    return jsonify(normalize_id(new_el)), 200


@election_blueprint.route("<string:election_id>/patch", methods=["POST"])
@jwt_required
@schema_validator(update_election_info)
def patch_el_info(election_id):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info(f"Patch request to unknown election {election_id}")
        return "Error", 404

    client["elections"]["meta"].find_one_and_update(
        {"_id": ObjectId(election_id)},
        {"$set": request.get_json()}
    )

    return "OK", 200


@election_blueprint.route("<string:election_id>/delete", methods=["POST"])
@jwt_required
@schema_validator(delete_election)
def del_election(election_id):
    election_to_delete = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    if not election_to_delete:
        logger.info("Delete request to unknown election " + election_id)
        return "Error", 404

    client["elections"]["meta"].delete_one({"_id": ObjectId(election_id)})

    client["elections"]["banned" + election_id].drop()
    client["elections"]["voted" + election_id].drop()
    client["elections"]["normal" + election_id].drop()

    logger.info(
        f"Election {election_id} with name {election_to_delete['name']} was deleted")

    return "OK", 200


@election_blueprint.route("/<string:election_id>/vote/new", methods=["POST"])
@jwt_required
def add_opt(election_id):
    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    if not election:
        logger.info(f"Add vote request to unknown election {election_id}")
        return "Error", 404

    if election["state"] != "ongoing":
        logger.info(
            f"Add vote request to election {election_id} with state {election['state']}")
        return "Error", 403

    data = request.get_json()

    if data["type"] != election["type"]:
        logger.info("Wrong vote type on new vote")
        return "Error", 400

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
            "serviceLink": data.get("serviceLink", ""),
            "cutCommentary": data.get("cutCommentary", ""),
            "album": data.get("album", ""),
            "singer": data.get("singer", "")
        }

    new_id = client["elections"]["normal" +
                                 election_id].insert_one(new_vote).inserted_id

    new_vote["_id"] = new_vote

    return jsonify(normalize_id(new_vote)), 200  # TODO Test


@election_blueprint.route("/<string:election_id>/vote/<string:vote_id>", methods=["POST"])
@jwt_required
def add_vote(election_id: str, vote_id: str):
    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    if election is None:
        logger.info(f"Add vote request to unknown election {election_id}")
        return "Error", 404

    if election["state"] != "ongoing":
        logger.info(
            f"Add vote request to election {election_id} with state {election['state']}")
        return "Error", 403

    normal_object = client["elections"]["normal" + election_id].find_one(
        {"_id": ObjectId(vote_id)}
    )

    if not normal_object:
        banned_object_exists = client["elections"]["banned" + election_id].find_one(
            {"_id": ObjectId(vote_id)}
        )

        if banned_object_exists:
            logger.info(
                f"Vote request to banned option {vote_id} in election {election_id}")
            return "Error", 403

        logger.info(
            f"Vote request to unknown option {vote_id} in election {election_id}")
        return "Error", 404

    if get_jwt_identity()["name"] in normal_object["voters"]:
        logger.info(f"Add vote request to already voted resource {vote_id}")
        return "Error", 409

    client["elections"]["normal" + election_id].update_one(
        {"_id": ObjectId(vote_id)},
        {"$push": {"voters": get_jwt_identity()["name"]}}
    )

    return "OK", 200  # TODO Test


@election_blueprint.route("/<string:election_id>/unvote/<string:vote_id>", methods=["POST"])
@jwt_required
def remove_vote(election_id: str, vote_id: str):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info(f"Remove vote request to unknown election {election_id}")
        return "Error", 404

    normal_object = client["elections"]["normal" + election_id].find_one(
        {"_id": ObjectId(vote_id)}
    )

    if not normal_object:
        banned_object_exists = client["elections"]["banned" + election_id].find_one(
            {"_id": ObjectId(vote_id)}
        )

        if banned_object_exists:
            logger.info("Remove vote request to banned option " +
                        vote_id + " in election " + election_id)
            return "Error", 403

        logger.info("Remove vote request to unknown option " +
                    vote_id + " in election " + election_id)
        return "Error", 404

    if get_jwt_identity()["name"] not in normal_object["voters"]:
        logger.info(f"Remove vote request to not voted resource {vote_id}")
        return "Error", 409

    client["elections"]["normal" + election_id].update_one(
        {"_id": ObjectId(vote_id)},
        {"$pull": {"voters": get_jwt_identity()["name"]}}
    )

    return "OK", 200  # TODO Test


@election_blueprint.route("/<string:election_id>/voted")
@jwt_required
def list_voted(election_id: str):
    election_exists = client["elections"]["meta"].count_documents(
        {"_id": ObjectId(election_id)})

    if election_exists == 0:
        logger.info(f"List vote request to unknown election {election_id}")
        return "Error", 404

    votes = []
    user_id = get_jwt_identity()["name"]

    for cl_var in ["normal", "banned", "voted"]:
        for obj in client["elections"][cl_var + election_id].find({"voters": {"$in": [user_id]}}):
            votes.append(str(obj["_id"]))

    return jsonify(votes), 200


@election_blueprint.route("/getlast/")
def get_last():  # ОНО ТЕБЯ СОЖРЕТ Функции нет в документации, считайте, что тут ее тоже нет.
    number_of_elections = client["elections"]["meta"].count()

    if number_of_elections == 0:
        return "Error", 409

    election = client["elections"]["meta"].find_one({"state": "ongoing"})

    return fetch_election_by_meta(election)


@election_blueprint.route("/getlast/<string:election_type>")
def get_specific_last(election_type: str):
    number_of_elections = client["elections"]["meta"].count_documents(
        {"type": election_type})

    if number_of_elections == 0:
        return "Error", 409

    election = client["elections"]["meta"].find_one(
        {"state": "ongoing", "type": election_type})

    return fetch_election_by_meta(election)


@election_blueprint.route("/<string:election_id>/vote/<string:vote_id>/patch", methods=["POST"])
@jwt_required
def update_option(election_id: str, vote_id: str):
    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    if election is None:
        logger.info(f"Update vote request to unknown election {election_id}")
        return "Error", 404

    if election["state"] != "ongoing":
        logger.info(
            f"Update vote request to election {election_id} with state {election['state']}")
        return "Error", 403

    normal_object = client["elections"]["normal" + election_id].find_one(
        {"_id": ObjectId(vote_id)}
    )

    banned_object_exists = client["elections"]["banned" + election_id].find_one(
        {"_id": ObjectId(vote_id)}
    )

    to_move = None

    if banned_object_exists and request.get_json()["state"] == "normal":

        client["elections"]["banned" + election_id].update_one(
            {"_id": ObjectId(vote_id)},
            {"$set": request.get_json()}
        )

        to_move = client["elections"]["banned" + election_id].find_one(
            {"_id": ObjectId(vote_id)}
        )

        to_move["_id"] = str(to_move["_id"])
        client["elections"]["normal" + election_id].insert_one(to_move)
        client["elections"]["baned" + election_id].delete_one(
            {"_id": ObjectId(vote_id)}
        )

    if normal_object and request.get_json()["state"] == "banned":

        client["elections"]["normal" + election_id].update_one(
            {"_id": ObjectId(vote_id)},
            {"$set": request.get_json()}
        )

        to_move = client["elections"]["normal" + election_id].find_one(
            {"_id": ObjectId(vote_id)}
        )

        to_move["_id"] = str(to_move["_id"])
        client["elections"]["banned" + election_id].insert_one(to_move)
        client["elections"]["normal" + election_id].delete_one(
            {"_id": ObjectId(vote_id)}
        )

    return jsonify(
        normalize_id(
            to_move or client["elections"]["normal" + election_id].find_one(
                {"_id": ObjectId(vote_id)}
            )
        )
    ), 200


@election_blueprint.route("/find/<string:el_type>", methods=["GET"])
def get_elections(el_type):
    out = []

    for item in client["elections"]["meta"].find({"type": el_type}).sort("datetime"):
        out.append(normalize_id(item))

    return jsonify(out)
