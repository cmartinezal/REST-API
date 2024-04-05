"""
Endpoints for Superpowers
"""
import json
from flask import Blueprint, jsonify, request
from .helpers import *
from ...utils.database import get_db_data_by_value

blueprint = Blueprint('superpowers', __name__, url_prefix='/api/v1')


@blueprint.route('/superpowers', methods=['GET', 'POST'])
def superpowers() -> dict:
    """Get a list of Superpowers or create new"""

    if request.method == "GET":
        return get_superpowers()

    if request.method == "POST":
        body = request.get_json()
        return post_superpower(body)


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
        body = json.loads(request.data)
        return put_superpower(body, query, id)

    if request.method == "DELETE":
        return delete_superpower(id)
