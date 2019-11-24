from pymongo import MongoClient
from loguru import logger
from flask import Blueprint, request, Response, jsonify
from owo.api.utils import schema_validator, validate_ej
from owo.security.hashing import hash_new_password
import owo.api.schemas as schemas


logger.add("api_user.log", colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day",
           backtrace=True, diagnose=True)

client = MongoClient('mongodb://mongo:27017/', connect=False)
user = Blueprint('page', __name__)


@user.route("/user", methods=["post"])
@schema_validator(schemas.add_user)
def add_user(): # TODO Поправить методы логина в соответсвии с методами ЭЖ
    raise NotImplementedError
    data = request.get_json()
    if not validate_ej(data["ejlogin"], data["ejpassword"]):
        return (
            {
                "message": "Wrong EJ login/pass",
                "code": 400
            },
            400
        )

    if client["meta"]["users"].count_documents({"login": data["login"]}):
        return (
            {
                "message": "User with such login exists",
                "code": 400
            },
            400
        )

    if client["meta"]["users"].count_documents({"ejlogin": data["ejlogin"]}):
        return (
            {
                "message": "User with such ejlogin exists",
                "code": 400
            },
            400
        )

    client["meta"]["users"].insert_one(
        {
            "login": data["login"],
            "hpassword": hash_new_password(data["password"]),
            "ejtoken": None,
            "type": "ok",
            "state": "normal"
        }
    )

    return Response(
        status=200
    )


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
