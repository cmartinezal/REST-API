"""
Endpoints for superpowers
"""
import json
from flask import Blueprint, Flask, jsonify, request
from helpers.functions import get_db_data, get_db_data_by_value, body_is_valid, insert_row, update_row, delete_row

blueprint = Blueprint('superpowers', __name__, url_prefix='/api/v1')


@blueprint.route('/superpowers', methods=['GET', 'POST'])
def superpowers() -> dict:
    """Get a list of Superpowers or create new"""

    if request.method == "GET":
        query = """
        SELECT id, name, created_date FROM SUPERPOWERS;
        """
        superpower_list = get_db_data(query)

        if superpower_list is None or len(superpower_list) == 0:
            return jsonify({'error': 'Superpowers not found.'}), 404

        if 'error' in superpower_list:
            return superpower_list, 500

        return jsonify(superpower_list)

    if request.method == "POST":
        select_query = """
        SELECT id, name, created_date FROM SUPERPOWERS where id = (SELECT MAX(id) from SUPERPOWERS);
        """
        superpower_body = request.get_json()
        if not superpower_body or not body_is_valid(superpower_body):
            return jsonify({'error': 'Invalid Superpower properties.'}), 400
        name = superpower_body.get("name", "")
        response = insert_row(
            'INSERT INTO SUPERPOWERS(name) VALUES (?);', [name], select_query)

        if response and 'error' in response:
            return response, 500

        return jsonify(response[0]), 201


@blueprint.route('/superpowers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def superpower(id: int) -> dict:
    """Get, update or delete existing Superpowers"""

    query = """
    SELECT id, name, created_date FROM SUPERPOWERS WHERE id = ?;
    """

    superpower_list = get_db_data_by_value(query, [id])

    if superpower_list is None or len(superpower_list) == 0:
        return jsonify({'error': 'Superpower not found.'}), 404

    if 'error' in superpower_list:
        return superpower_list, 500

    if request.method == "GET":
        return jsonify(superpower_list[0])

    if request.method == "PUT":
        updated_superpower = json.loads(request.data)
        if not body_is_valid(updated_superpower):
            return jsonify({'error': 'Invalid Superpower properties.'}), 400
        response = update_row(
            'UPDATE SUPERPOWERS SET name=? WHERE id=?;', updated_superpower["name"], id, query)

        if response and 'error' in response:
            return response, 500

        return jsonify(response[0])

    if request.method == "DELETE":
        delete_row(
            'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superpower_id=?;', [id])
        delete_row(
            'DELETE FROM SUPERPOWERS WHERE id=?;', [id])
        return '', 204
