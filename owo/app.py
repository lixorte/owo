from owo.api.user import user
from owo.api.election import election_blueprint
from owo.api.testing import tesing_blueprint
from owo.front.main import front_blueprint
from loguru import logger
import os
from flask_cors import CORS
from flask import Flask
from flask_jwt_extended import JWTManager

logger.add(__name__, colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day",
           backtrace=True, diagnose=True)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]
app.config["JWT_TOKEN_LOCATION"] = ('cookies', 'headers')
app.config["DOMAIN"] = "http://" + os.environ["DOMAIN"]

jwt = JWTManager(app)
CORS(app)

app.register_blueprint(user)
app.register_blueprint(election_blueprint)
app.register_blueprint(front_blueprint)

if os.environ["DEBUG"] == "TRUE":
    app.register_blueprint(tesing_blueprint)


if __name__ == "__main__":
    app.run()
