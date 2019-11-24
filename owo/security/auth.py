import pymongo
from bson.objectid import ObjectId

from owo.security.hashing import is_correct_password

client = pymongo.MongoClient("mongo", 27017, connect=False)


class DummyJWT:
    def __init__(self, id):
        super().__init__()
        self.id = id


def authenticate(username: str, password: str):
    user = client["meta"]["users"].find_one({"login": username})

    if user is None:
        return False

    if not is_correct_password(user["hpassword"], password):
        return False

    out = DummyJWT(
        str(user["_id"])
    )

    return out


def identity(payload):
    user = client["meta"]["users"].find_one(
        {"_id": ObjectId(payload["identity"])}
    )
    user["id"] = user["_id"]
    return user
