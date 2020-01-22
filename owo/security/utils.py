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
        ("client_id", DEV_ID),
        ("code", code),
        ("redirect_uri", redirect_uri)
    ]
    req = requests.get("http://auth.eljur.ru/oauthtoken", params=query)

    if not req.ok:
        logger.info(
            f"Got {req.status_code} with " +
            f"response {req.json()}"
        )
        raise ValueError

    return req.json()["access_token"]


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

    if not req.ok:
        logger.info(
            f"Got {req.status_code} with " +
            f"error {req.json()['response']['error']}"
        )
        raise ValueError

    return req.json()["response"]["result"]
