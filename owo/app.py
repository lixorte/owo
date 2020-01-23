from owo.security.auth import get_identity, user_exists, create_user
from owo.api.user import user
from owo.api.election import election_blueprint
from owo.api.testing import tesing_blueprint
from loguru import logger
import os
import pymongo
from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, set_access_cookies,
                                set_refresh_cookies)


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]
app.config["JWT_TOKEN_LOCATION"] = ('cookies', 'headers')
OAUTH_REDIRECT = "/auth"
DOMAIN = "http://" + os.environ["DOMAIN"]
jwt = JWTManager(app)
client = pymongo.MongoClient("mongo", 27017, connect=False)

logger.add(__name__, colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day",
           backtrace=True, diagnose=True)

app.register_blueprint(user)
app.register_blueprint(election_blueprint)

if os.environ["DEBUG"] == "TRUE":
    app.register_blueprint(tesing_blueprint)


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

    session_user = client["meta"]["users"].find_one(
        {"name": user_rules["name"]})
    del session_user["_id"]

    access_token = create_access_token(identity=session_user)
    refresh_token = create_refresh_token(identity=session_user)

    resp = make_response(redirect(state))

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


@app.route("/")
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
