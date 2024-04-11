
"""
Helper functions for Superpowers    
"""

from flask import jsonify
from ...utils.validations import validate_name_body
from ...utils.database import get_db_data, insert_row, update_row, delete_row


def get_superpowers() -> dict:
    """Get all Superpowers"""

    query = """
    SELECT id, name, created_date FROM SUPERPOWERS;
    """
    superpower_list = get_db_data(query)

    if superpower_list is None or len(superpower_list) == 0:
        return jsonify({'error': 'Superpowers not found.'}), 404

    if 'error' in superpower_list:
        return superpower_list, 500

    return jsonify(superpower_list)


def post_superpower(body: dict) -> dict:
    """Create new Superpower"""

    select_query = """
    SELECT id, name, created_date FROM SUPERPOWERS where id = (SELECT MAX(id) from SUPERPOWERS);
    """

    if not body or not validate_name_body(body):
        return jsonify({'error': 'Invalid Superpower properties.'}), 400
    name = body.get("name", "")
    response = insert_row(
        'INSERT INTO SUPERPOWERS(name) VALUES (?);', [name], select_query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0]), 201


def put_superpower(body: dict, query: str, id: int) -> dict:
    """Update Superpower"""

    if not validate_name_body(body):
        return jsonify({'error': 'Invalid Superpower properties.'}), 400
    response = update_row(
        'UPDATE SUPERPOWERS SET name=? WHERE id=?;', [body["name"], id], id, query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0])


def delete_superpower(id: int) -> dict:
    """Delete Superpower"""

    delete_row(
        'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superpower_id=?;', [id])
    delete_row(
        'DELETE FROM SUPERPOWERS WHERE id=?;', [id])
    return '', 204
