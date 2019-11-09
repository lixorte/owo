import pymongo
from bson.objectid import ObjectId

from owo.security.hashing import is_correct_password

CLIENT = pymongo.MongoClient("mongo", 27017)
DATABASE = CLIENT["database"]
USERS = DATABASE["users"]


def authenticate(username: str, password: str):
    user = USERS.find_one({"username": username})

    if user is None:
        return False

    if not is_correct_password(user["pw_hash"], password):
        return False

    user["id"] = user["_id"]

    return user


def identity(payload):
    user = USERS.find_one({"_id": ObjectId(payload["identity"])})
    user["id"] = user["_id"]
    return user
