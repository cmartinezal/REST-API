import json
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from helpers.functions import get_db_data, get_db_data_by_value, superhero_is_valid, insert_row, update_row, delete_row
from blueprints.v1.superheroes import blueprint as superhero_endpoints


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
app.register_blueprint(superhero_endpoints)

if __name__ == '__main__':
    app.run(debug=True)
