import json
from flask import Blueprint, Flask, jsonify, request
from helpers.functions import get_db_data, get_db_data_by_value, body_is_valid, insert_row, update_row, delete_row

blueprint = Blueprint('superheroes', __name__, url_prefix='/api/v1')


@blueprint.route('/superheroes', methods=['GET', 'POST'])
def superheroes() -> dict:
    """Get a list of superheroes or create new"""

    if request.method == "GET":
        query = """
        SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
        FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
        LEFT JOIN SUPERPOWERS P ON P.id=HP.superpower_id
        GROUP BY H.id, H.name, H.created_date;
        """
        superhero_list = get_db_data(query)
        if superhero_list is None or len(superhero_list) == 0:
            return jsonify({'error': 'superheroes not found.'}), 404
        return jsonify(superhero_list)

    if request.method == "POST":
        select_query = """
        SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
        FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
        LEFT JOIN SUPERPOWERS P ON P.id=HP.superpower_id WHERE H.id = (SELECT MAX(id) FROM SUPERHEROES)
        GROUP BY H.id, H.name, H.created_date;
        """
        superhero_body = request.get_json()
        if not superhero_body or not body_is_valid(superhero_body):
            return jsonify({'error': 'Invalid superhero properties.'}), 400
        name = superhero_body.get("name", "")
        new_superhero = insert_row(
            'INSERT INTO SUPERHEROES(name) VALUES (?);', name, select_query)
        return jsonify(new_superhero[0]), 201


@blueprint.route('/superheroes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def superhero(id: int) -> dict:
    """Get, update or delete existing superhero"""

    query = """
    SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
    FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
    LEFT JOIN SUPERPOWERS P ON P.id=HP.superpower_id WHERE H.id = ?
    GROUP BY H.id, H.name, H.created_date;
    """

    superhero_list = get_db_data_by_value(query, id)

    if superhero_list is None or len(superhero_list) == 0:
        return jsonify({'error': 'superhero not found.'}), 404

    if request.method == "GET":
        return jsonify(superhero_list[0])

    if request.method == "PUT":
        updated_superhero = json.loads(request.data)
        if not body_is_valid(updated_superhero):
            return jsonify({'error': 'Invalid superhero properties.'}), 400
        superhero_list = update_row(
            'UPDATE SUPERHEROES SET name=? WHERE id=?;', updated_superhero["name"], id, query)
        return jsonify(superhero_list[0])

    if request.method == "DELETE":
        delete_row(
            'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superhero_id=?;', id)
        delete_row(
            'DELETE FROM SUPERHEROES WHERE id=?;', id)
        return '', 204
