"""
Helper functions for Users
"""

from werkzeug.security import generate_password_hash
from flask import jsonify
from typing import List
from ...utils.validations import validate_user_body
from ...utils.database import get_db_data, insert_row, update_row, delete_row


def get_users() -> dict:
    """Get all Users"""

    query = """
    SELECT U.id, U.first_name, U.last_name, U.email, U.created_date FROM USERS U;
    """
    user_list = get_db_data(query)

    if user_list is None or len(user_list) == 0:
        return jsonify({'error': 'users not found.'}), 404

    if 'error' in user_list:
        return user_list, 500

    return jsonify(user_list)


def post_user(body: dict) -> dict:
    """Create a new User"""

    select_query = """
    SELECT U.id, U.first_name, U.last_name, U.email, U.created_date FROM USERS U WHERE U.id = (SELECT MAX(id) FROM USERS);
    """
    if not body or not validate_user_body(body):
        return jsonify({'error': 'Invalid User properties.'}), 400

    first_name = body.get("first_name", "")
    last_name = body.get("last_name", "")
    email = body.get("email", "")
    password = generate_password_hash(body.get("password", ""))
    response = insert_row(
        'INSERT INTO USERS(first_name, last_name, email, password) VALUES (?, ?, ?, ?);', [first_name, last_name, email, password], select_query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0]), 201


def put_user(body: dict, query: str, id: int) -> dict:
    """Update a User"""

    if not validate_user_body(body):
        return jsonify({'error': 'Invalid User properties.'}), 400

    first_name = body.get("first_name", "")
    last_name = body.get("last_name", "")
    email = body.get("email", "")
    password = generate_password_hash(body.get("password", ""))

    update_query = """
    UPDATE USERS SET
    first_name = ?, last_name = ?, email = ?, password = ?
    WHERE id = ?;
    """
    response = update_row(
        update_query, [first_name, last_name, email, password, id], id, query)

    if response and 'error' in response:
        return response, 500

    return jsonify(response[0])


def delete_user(id: int) -> dict:
    """Delete a User"""

    delete_row(
        'DELETE FROM USERS WHERE id = ?;', [id])
    return '', 204
