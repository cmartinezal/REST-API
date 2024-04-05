
"""
Helper functions for Superheroes
"""
import json
from flask import jsonify, request
from typing import List
from ...utils.validations import body_is_valid
from ...utils.database import get_db_data, get_db_data_by_value, insert_row, update_row, delete_row


def get_superheroes() -> dict:
    """Get all Superheroes"""

    query = """
    SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
    FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
    LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id
    GROUP BY H.id, H.name, H.created_date;
    """
    superhero_list = get_db_data(query)

    if superhero_list is None or len(superhero_list) == 0:
        return jsonify({'error': 'superheroes not found.'}), 404

    if 'error' in superhero_list:
        return superhero_list, 500

    return jsonify(superhero_list)


def post_superhero(superhero_body: dict) -> dict:
    """Create a new Superhero"""

    select_query = """
    SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
    FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
    LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id WHERE H.id = (SELECT MAX(id) FROM SUPERHEROES)
    GROUP BY H.id, H.name, H.created_date;
    """
    if not superhero_body or not body_is_valid(superhero_body):
        return jsonify({'error': 'Invalid Superhero properties.'}), 400

    name = superhero_body.get("name", "")
    response = insert_row(
        'INSERT INTO SUPERHEROES(name) VALUES (?);', [name], select_query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0]), 201


def put_superhero(body: dict, query: str, id: int) -> dict:
    """Update a Superhero"""

    if not body_is_valid(body):
        return jsonify({'error': 'Invalid Superhero properties.'}), 400
    response = update_row(
        'UPDATE SUPERHEROES SET name=? WHERE id=?;', body["name"], id, query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0])


def delete_superhero(id: int) -> dict:
    """Delete a Superhero"""

    delete_row(
        'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superhero_id = ?;', [id])
    delete_row(
        'DELETE FROM SUPERHEROES WHERE id = ?;', [id])
    return '', 204


def get_superhero_superpowers(query: str, id: int) -> dict:
    """Get Superhero Superpowers"""

    superpower_list = get_db_data_by_value(query, [id])

    if superpower_list is None or len(superpower_list) == 0:
        return jsonify({'error': 'Superhero has no Superpowers.'}), 404

    if 'error' in superpower_list:
        return superpower_list, 500

    return jsonify(superpower_list)


def post_superhero_superpower(superpower: List[dict], body: dict, query: str, id: int) -> dict:
    """Add Superpower to Superhero"""

    if superpower and len(superpower) > 0:
        return jsonify({'error': 'Superhero already has this Superpower.'}), 400

    response = insert_row(
        'INSERT INTO SUPERHERO_SUPERPOWERS(superhero_id, superpower_id) VALUES (?, ?);',
        [id, body['id']], query, [id])

    if response and 'error' in response:
        return response, 500

    return jsonify(response), 201


def delete_superhero_superpower(superpower: List[dict], body: dict, id: int) -> dict:
    """Delete Superhero Superpower"""

    if superpower is None or len(superpower) == 0:
        return jsonify({'error': 'Superhero does not have this Superpower.'}), 404
    delete_row(
        'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superhero_id = ? AND superpower_id = ?;',
        [id, body['id']])
    return '', 204


def superhero_exists(id: int) -> dict:
    """Check if Superhero exists"""

    superhero_query = """
    SELECT H.id
    FROM SUPERHEROES H
    WHERE H.id = ?;
    """

    superhero_data = get_db_data_by_value(superhero_query, [id])

    if superhero_data is None or len(superhero_data) == 0 or 'error' in superhero_data:
        return False
    return True


def superpower_exists(id: int) -> dict:
    """Check if Superpower exists"""

    select_query = 'SELECT id FROM SUPERPOWERS WHERE id = ?'
    superpower = get_db_data_by_value(select_query, [id])

    if superpower is None or len(superpower) == 0 or 'error' in superpower:
        return False
    return True
