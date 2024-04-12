
"""
Endpoints for Users
"""
import json
from flask import Blueprint, jsonify, request
from ...utils.database import get_db_data_by_value
from .helpers import *
from flask_jwt_extended import jwt_required

blueprint = Blueprint('users', __name__, url_prefix='/api/v1')


@blueprint.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users() -> dict:
    """Get a list of users or create new"""

    if request.method == "GET":
        return get_users()

    if request.method == "POST":
        body = request.get_json()
        return post_user(body)


@blueprint.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user(id: int) -> dict:
    """Get, update or delete existing User"""

    query = """
    SELECT U.id, U.first_name, U.last_name, U.email, U.created_date FROM USERS U WHERE U.id = ?;
    """

    user_list = get_db_data_by_value(query, [id])

    if user_list is None or len(user_list) == 0:
        return jsonify({'error': 'User not found.'}), 404

    if 'error' in user_list:
        return user_list, 500

    if request.method == "GET":
        return jsonify(user_list[0])

    if request.method == "PUT":
        body = json.loads(request.data)
        return put_user(body, query, id)

    if request.method == "DELETE":
        return delete_user(id)
