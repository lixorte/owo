import os

from flask import Flask
from flask_jwt import JWT

from owo.security.auth import authenticate, identity
from owo.api.user import user

app = Flask(__name__)
app.secret_key = os.environ["JWT_SECRET"]
jwt = JWT(app, authenticate, identity)

app.register_blueprint(user)

if __name__ == "__main__":
    app.run()
