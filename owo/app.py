from owo.security.auth import get_identity, user_exists, create_user
from owo.api.user import user
import os

import pymongo
from flask import Flask, request, jsonify, make_response, render_template
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, set_access_cookies,
                                set_refresh_cookies)


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]
OAUTH_REDIRECT = "/auth"
DOMAIN = os.environ["DOMAIN"]
jwt = JWTManager(app)
client = pymongo.MongoClient("mongo", 27017, connect=False)


app.register_blueprint(user)


@app.route(OAUTH_REDIRECT, methods=["GET"])
def oauth_handler():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return jsonify(
            {
                "message": "Invalid query",
                "code": 400
            }
        ), 400

    try:
        user_rules = get_identity(code, DOMAIN+OAUTH_REDIRECT)
    except ValueError:
        return jsonify(
            {
                "message": "Wrong code",
                "code": 401
            }
        ), 401

    if not user_exists(user_rules["name"]):
        create_user(user_rules["name"], user_rules["title"])

    session_user = client["meta"]["users"].get_one({"name": user_rules["name"]})
    del session_user["_id"]

    access_token = create_access_token(identity=session_user)
    refresh_token = create_refresh_token(identity=session_user)

    resp = make_response(render_template("index.html"))

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


if __name__ == "__main__":
    app.run()
