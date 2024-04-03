import json
from flask import Blueprint, Flask, jsonify, request
from helpers.functions import get_db_data, get_db_data_by_value, superhero_is_valid, insert_row, update_row, delete_row

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/superheroes', methods=['GET', 'POST'])
def superheroes() -> dict:
    """Get a list of superheroes or create new"""

    if request.method == "GET":
        superheroes = get_db_data('SELECT * FROM SUPERHEROES;')
        if superheroes is None or len(superheroes) == 0:
            return jsonify({'error': 'superheroes not found.'}), 404
        return jsonify(superheroes)

    if request.method == "POST":
        superhero = request.get_json()
        if not superhero or not superhero_is_valid(superhero):
            return jsonify({'error': 'Invalid superhero properties.'}), 400
        name = superhero.get("name", "")
        new_superhero = insert_row(
            'INSERT INTO SUPERHEROES(name) VALUES (?);', name)
        return jsonify(new_superhero), 201


@blueprint.route('/superheroes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def superheroe(id: int) -> dict:
    """Update existing superhero"""

    superhero = get_db_data_by_value(
        'SELECT * FROM SUPERHEROES WHERE id=?;', id)

    if superhero is None or len(superhero) == 0:
        return jsonify({'error': 'superhero not found.'}), 404

    if request.method == "GET":
        return jsonify(superhero)

    if request.method == "PUT":
        updated_superhero = json.loads(request.data)
        if not superhero_is_valid(updated_superhero):
            return jsonify({'error': 'Invalid superhero properties.'}), 400
        superhero = update_row(
            'UPDATE SUPERHEROES SET name=? WHERE id=?;', updated_superhero["name"], id)
        return jsonify(superhero)

    if request.method == "DELETE":
        delete_row(
            'DELETE FROM SUPERHEROES WHERE id=?;', id)
        return jsonify(superhero), 200
