import json
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from helpers.functions import get_db_data, get_db_data_by_value, superhero_is_valid, insert_row, update_row, delete_row


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


@app.route('/superheroes', methods=['GET'])
def get_superheroes() -> dict:
    """Get a list of superheroes"""

    superheroes = get_db_data('SELECT * FROM SUPERHEROES;')
    if superheroes is None:
        return jsonify({'error': 'superheroes not found.'}), 404
    return jsonify(superheroes)


@app.route('/superheroes/<int:id>', methods=['GET'])
def get_superheroe_by_id(id: int) -> dict:
    """Get superhero by id"""

    superhero = get_db_data_by_value(
        'SELECT * FROM SUPERHEROES WHERE id=?;', id)
    if superhero is None:
        return jsonify({'error': 'superhero not found.'}), 404
    return jsonify(superhero)


@app.route('/superheroes', methods=['POST'])
def create_superheroe() -> dict:
    """Add new superhero"""
    superhero = request.get_json()
    print(superhero)
    if not superhero or not superhero_is_valid(superhero):
        return jsonify({'error': 'Invalid superhero properties.'}), 400
    name = superhero.get("name", "")
    new_superhero = insert_row(
        'INSERT INTO SUPERHEROES(name) VALUES (?);', name)
    return jsonify(new_superhero), 201


@app.route('/superheroes/<int:id>', methods=['PUT'])
def update_superhero(id: int) -> dict:
    """Update existing superhero"""

    superhero = get_db_data_by_value(
        'SELECT * FROM SUPERHEROES WHERE id=?;', id)

    if superhero is None:
        return jsonify({'error': 'superhero not found.'}), 404

    updated_superhero = json.loads(request.data)
    if not superhero_is_valid(updated_superhero):
        return jsonify({'error': 'Invalid superhero properties.'}), 400

    superhero = update_row(
        'UPDATE SUPERHEROES SET name=? WHERE id=?;', updated_superhero["name"], id)

    return jsonify(superhero)


@app.route('/superheroes/<int:id>', methods=['DELETE'])
def delete_superhero(id: int) -> dict:
    """Delete existing superhero"""

    superhero = get_db_data_by_value(
        'SELECT * FROM SUPERHEROES WHERE id=?;', id)
    if superhero is None:
        return jsonify({'error': 'superhero not found.'}), 404

    delete_row(
        'DELETE FROM SUPERHEROES WHERE id=?;', id)
    return jsonify(superhero), 200


if __name__ == '__main__':
    app.run(debug=True)
