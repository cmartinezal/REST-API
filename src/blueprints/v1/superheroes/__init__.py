
"""
Endpoints for superheroes
"""
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
        LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id
        GROUP BY H.id, H.name, H.created_date;
        """
        superhero_list = get_db_data(query)

        if superhero_list is None or len(superhero_list) == 0:
            return jsonify({'error': 'superheroes not found.'}), 404

        if 'error' in superhero_list:
            return superhero_list, 500

        return jsonify(superhero_list)

    if request.method == "POST":
        select_query = """
        SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
        FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
        LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id WHERE H.id = (SELECT MAX(id) FROM SUPERHEROES)
        GROUP BY H.id, H.name, H.created_date;
        """
        superhero_body = request.get_json()
        if not superhero_body or not body_is_valid(superhero_body):
            return jsonify({'error': 'Invalid Superhero properties.'}), 400

        name = superhero_body.get("name", "")
        response = insert_row(
            'INSERT INTO SUPERHEROES(name) VALUES (?);', [name], select_query)

        if response and 'error' in response:
            return response, 500

        return jsonify(response[0]), 201


@blueprint.route('/superheroes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def superhero(id: int) -> dict:
    """Get, update or delete existing Superhero"""

    query = """
    SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,', ') as superpowers
    FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
    LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id WHERE H.id = ?
    GROUP BY H.id, H.name, H.created_date;
    """

    superhero_list = get_db_data_by_value(query, [id])

    if superhero_list is None or len(superhero_list) == 0:
        return jsonify({'error': 'Superhero not found.'}), 404

    if 'error' in superhero_list:
        return superhero_list, 500

    if request.method == "GET":
        return jsonify(superhero_list[0])

    if request.method == "PUT":
        updated_superhero = json.loads(request.data)
        if not body_is_valid(updated_superhero):
            return jsonify({'error': 'Invalid Superhero properties.'}), 400
        response = update_row(
            'UPDATE SUPERHEROES SET name=? WHERE id=?;', updated_superhero["name"], id, query)

        if response and 'error' in response:
            return response, 500

        return jsonify(response[0])

    if request.method == "DELETE":
        delete_row(
            'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superhero_id=?;', [id])
        delete_row(
            'DELETE FROM SUPERHEROES WHERE id=?;', [id])
        return '', 204


@blueprint.route('/superheroes/<int:id>/superpowers', methods=['GET', 'POST', 'DELETE'])
def superhero_superpowers(id: int) -> dict:
    """Get, create or delete Superhero superpowers"""

    superhero_query = """
    SELECT H.id
    FROM SUPERHEROES H
    WHERE H.id = ?;
    """

    query = """
    SELECT P.id, P.name, P.created_date
    FROM SUPERPOWERS P, SUPERHERO_SUPERPOWERS HP 
    WHERE P.id = HP.superpower_id AND HP.superhero_id = ?;
    """

    superhero_data = get_db_data_by_value(superhero_query, [id])

    if superhero_data is None or len(superhero_data) == 0:
        return jsonify({'error': 'Superhero not found.'}), 404

    if 'error' in superhero_data:
        return superhero_data, 500

    if request.method == "GET":
        superpower_list = get_db_data_by_value(query, [id])

        if superpower_list is None or len(superpower_list) == 0:
            return jsonify({'error': 'Superhero has no superpowers.'}), 404

        if 'error' in superpower_list:
            return superpower_list, 500

        return jsonify(superpower_list)

    body = json.loads(request.data)
    if not body_is_valid(body, True):
        return jsonify({'error': 'Invalid superpower properties.'}), 400

    select_query = 'SELECT id FROM SUPERPOWERS WHERE id = ?'
    superpower = get_db_data_by_value(select_query, [body['id']])

    if superpower is None or len(superpower) == 0:
        return jsonify({'error': 'Superpower not found.'}), 404

    if 'error' in superpower:
        return superpower, 500

    select_query = """
    SELECT P.id
    FROM SUPERPOWERS P, SUPERHERO_SUPERPOWERS HP 
    WHERE P.id = HP.superpower_id AND HP.superhero_id = ? AND P.ID = ?;
    """
    superpower = get_db_data_by_value(select_query, [id, body['id']])

    print(superpower)

    if superpower and 'error' in superpower:
        return superpower, 500

    if request.method == "POST":
        if superpower and len(superpower) > 0:
            return jsonify({'error': 'Superhero already has this Superpower.'}), 400

        response = insert_row(
            'INSERT INTO SUPERHERO_SUPERPOWERS(superhero_id, superpower_id) VALUES (?, ?);',
            [id, body['id']], query, [id])

        if response and 'error' in response:
            return response, 500

        return jsonify(response[0], 201)

    if request.method == "DELETE":
        if superpower is None or len(superpower) == 0:
            return jsonify({'error': 'Superhero does not have this Superpower.'}), 404
        delete_row(
            'DELETE FROM SUPERHERO_SUPERPOWERS WHERE superhero_id = ? AND superpower_id = ?;', [id, body['id']])
        return '', 204
