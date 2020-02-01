from flask import Blueprint, render_template, make_response, jsonify, request, current_app, redirect
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from owo.security.auth import get_identity, user_exists, create_user
import pymongo

front_blueprint = Blueprint('front', __name__)
client = pymongo.MongoClient("mongo", 27017, connect=False)


@front_blueprint.route("/")
def main_page():
    return render_template("index.html")


@front_blueprint.route("/addsong.html")
def addsong():
    return render_template("addsong.html")


@front_blueprint.route("/adminusers.html")
def adminusers():
    return render_template("adminusers.html")


@front_blueprint.route("/adminvotings.html")
def adminvoting():
    return render_template("adminvotings.html")


@front_blueprint.route("/themevoting.html")
def themevoting():
    return render_template("themevoting.html")


@front_blueprint.route("/auth", methods=["GET"])
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
        user_rules = get_identity(code, current_app.config["DOMAIN"]+"/auth")
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
    resp.set_cookie("isAdmin", "true" if session_user["state"] == "admin" else "false")

    return resp, 200
