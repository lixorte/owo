from voluptuous import Schema, MultipleInvalid
import flask
from pymongo import MongoClient
from bson import ObjectId
from loguru import logger
import functools
from flask_jwt_extended import get_jwt_identity

client = MongoClient('mongodb://mongo:27017/', connect=False)


def schema_validator(schema: Schema):
    """Checks that combination of query and json content matches the schema"""
    def _validator(f):
        @functools.wraps(f)
        def __validator(*args, **kwargs):
            json_data = flask.request.get_json() or {}

            query_data = flask.request.args or {}

            to_check = dict(
                (k, v) for d in (json_data, query_data) for k, v in d.items()
            )

            try:
                schema(to_check)
            except MultipleInvalid:
                logger.warning(f"Dropped invalid request on {f.__name__}")
                return flask.jsonify(
                    {
                        "message": "Invalid schema",
                        "code": 400
                    }
                ), 400
            return f(*args, **kwargs)
        return __validator
    return _validator


def normalize_id(to_normalize: dict) -> dict:
    to_normalize["id"] = str(to_normalize["_id"])
    del to_normalize["_id"]
    return to_normalize


def fetch_election(election_id: str) -> dict:
    election = client["elections"]["meta"].find_one(
        {"_id": ObjectId(election_id)})

    del election["_id"]
    election["id"] = election_id

    normal_objects = [normalize_id(el)
                      for el in client["elections"]["normal"+election_id].find()]
    voted_objects = [normalize_id(el)
                     for el in client["elections"]["voted"+election_id].find()]
    banned_objects = [normalize_id(el)
                      for el in client["elections"]["banned"+election_id].find()]

    response = {
        "electionInfo": election,
        "normalObjects": normal_objects,
        "votedObjects": voted_objects,
        "bannedObjects": banned_objects
    }

    return response


def fetch_election_by_meta(election: dict) -> dict:
    election_id = str(election["_id"])
    del election["_id"]
    election["id"] = election_id

    normal_objects = [normalize_id(el)
                      for el in client["elections"]["normal"+election_id].find()]
    voted_objects = [normalize_id(el)
                     for el in client["elections"]["voted"+election_id].find()]
    banned_objects = [normalize_id(el)
                      for el in client["elections"]["banned"+election_id].find()]

    for coll in [normal_objects, voted_objects, banned_objects]:
        for opt in coll:
            opt["votes"] = len(opt["voters"])

    response = {
        "electionInfo": election,
        "normalObjects": normal_objects,
        "votedObjects": voted_objects,
        "bannedObjects": banned_objects
    }

    return response


def prefs_validator(prefs: dict):
    """
    Validates that request's author cookie has certain prefs
    """
    def _validator(f):
        @functools.wraps(f)
        def __validator(*args, **kwargs):
            user_data = get_jwt_identity()
            for key, item in prefs.items():
                if user_data.get(key, "") != item:
                    return flask.jsonify(
                        {
                            "message": "Invalid JWT prefs",
                            "code": 403
                            }
                        ), 403
            return f(*args, **kwargs)
        return __validator
    return _validator

