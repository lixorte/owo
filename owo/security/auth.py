import pymongo
from owo.security.utils import get_rules

client = pymongo.MongoClient("mongo", 27017, connect=False)


def get_identity(code: str, redirect_uri: str) -> dict:
    return get_rules(code, redirect_uri)


def user_exists(name: str) -> bool:
    return bool(client["meta"]["users"].count({"name": name}))


def create_user(name: str, title: str):
    client["meta"]["users"].insert_one(
        {
            "name": name,
            "titile": title,
            "type": "ok",
            "state": "normal"
        }
    )
