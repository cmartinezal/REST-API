import json
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from blueprints.v1.superheroes import blueprint as superhero_endpoints_v1
from blueprints.v1.superpowers import blueprint as superpower_endpoints_v1


app = Flask(__name__)
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Superhero API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(superhero_endpoints_v1)
app.register_blueprint(superpower_endpoints_v1)

if __name__ == '__main__':
    app.run(debug=True)
