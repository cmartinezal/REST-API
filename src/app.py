import os
import bcrypt
from flask import Flask
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from routes.v1.superheroes import blueprint as superhero_endpoints_v1
from routes.v1.superpowers import blueprint as superpower_endpoints_v1
from routes.v1.users import blueprint as user_endpoints_v1
from routes.v1.auth import blueprint as auth_endpoints_v1


app = Flask(__name__)

SECRET_KEY = bcrypt.hashpw(
    b"63a01ef2fc32945d768cb7c7aaa1b168", bcrypt.gensalt())

app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=20)
app.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Superhero API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(auth_endpoints_v1)
app.register_blueprint(user_endpoints_v1)
app.register_blueprint(superhero_endpoints_v1)
app.register_blueprint(superpower_endpoints_v1)

# admin@web.com/admin


if __name__ == "__main__":
    app.run()
