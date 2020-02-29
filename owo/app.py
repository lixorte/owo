from owo.api.user import user
from owo import JWT_SECRET_KEY, DOMAIN
from owo.api.election import election_blueprint
from owo.api.testing import tesing_blueprint
from owo.front.main import front_blueprint
from loguru import logger
import os
from flask import Flask, redirect, request
from flask_jwt_extended import JWTManager

logger.add(__name__, colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day",
           backtrace=True, diagnose=True)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ('cookies', 'headers')
app.config["DOMAIN"] = "http://" + DOMAIN

jwt = JWTManager(app)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(election_blueprint, url_prefix="/election")
app.register_blueprint(front_blueprint)

if os.environ["DEBUG"] == "TRUE":
    app.register_blueprint(tesing_blueprint)


    @app.before_request
    def before_request():
        print(f"{request.endpoint} {request.cookies} {request.data}")


@app.route("/index.html")
def index_redir():
    return redirect("/")


if __name__ == "__main__":
    app.run()
