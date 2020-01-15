import requests
import os
from loguru import logger

DEV_ID = os.environ["DEV_ID"]
DEV_KEY = os.environ["DEV_KEY"]
SCHOOL_DOMAIN = os.environ["SCHOOL_DOMAIN"]


def get_token(code: str, redirect_uri: str) -> str:
    query = [
        ("devkey", DEV_KEY),
        ("grant_type", "authorization_code"),
        ("clienta_id", DEV_ID),
        ("code", code),
        ("redirect_uri", redirect_uri)
    ]
    req = requests.get("https://auth.eljur.ru/oauthtoken", params=query)

    if req.status_code != 200 or "access_token" not in req.json():
        logger.info(
            f"Got {req.status_code} with" +
            f"error {req.json()['response']['error']}"
        )
        raise ValueError

    return req.json()["acess_token"]


def get_rules(code: str, redirect_uri: str) -> dict:
    query = [
        ("devkey", DEV_KEY),
        ("vendor", SCHOOL_DOMAIN),
        ("out_format", "json"),
        ("auth_token", get_token(code, redirect_uri))
    ]

    req = requests.get(
        f"https://{SCHOOL_DOMAIN}.eljur.ru/api/getrules",
        params=query
    )

    if req.status_code != 200:
        logger.info(
            f"Got {req.status_code} with" +
            f"error {req.json()['response']['error']}"
        )
        raise ValueError

    return req.json()["response"]["result"]
