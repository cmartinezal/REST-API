
"""
Endpoints for Superheroes
"""
import json
from flask import Blueprint, jsonify, request
from ...utils.database import get_db_data_by_value
from ...utils.validations import validate_id_body
from .helpers import *
from flask_jwt_extended import jwt_required


blueprint = Blueprint("superheroes", __name__, url_prefix="/api/v1")


@blueprint.route("/superheroes", methods=["GET", "POST"])
@jwt_required(fresh=True)
def superheroes() -> dict:
    """Get a list of superheroes or create new"""

    if request.method == "GET":
        return get_superheroes()

    if request.method == "POST":
        superhero_body = request.get_json()
        return post_superhero(superhero_body)


@blueprint.route("/superheroes/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required(fresh=True)
def superhero(id: int) -> dict:
    """Get, update or delete existing Superhero"""

    query = """
    SELECT H.id, H.name, H.created_date, GROUP_CONCAT(P.name,", ") as superpowers
    FROM SUPERHEROES H LEFT JOIN SUPERHERO_SUPERPOWERS HP ON H.id = HP.superhero_id
    LEFT JOIN SUPERPOWERS P ON P.id = HP.superpower_id WHERE H.id = ?
    GROUP BY H.id, H.name, H.created_date;
    """

    superhero_list = get_db_data_by_value(query, [id])

    if superhero_list is None or len(superhero_list) == 0:
        return jsonify({"error": "Superhero not found."}), 404

    if "error" in superhero_list:
        return superhero_list, 500

    if request.method == "GET":
        return jsonify(superhero_list[0])

    if request.method == "PUT":
        body = json.loads(request.data)
        return put_superhero(body, query, id)

    if request.method == "DELETE":
        return delete_superhero(id)


@blueprint.route("/superheroes/<int:id>/superpowers", methods=["GET", "POST", "DELETE"])
@jwt_required(fresh=True)
def superhero_superpowers(id: int) -> dict:
    """Get, create or delete Superhero Superpowers"""

    query = """
    SELECT P.id, P.name, P.created_date
    FROM SUPERPOWERS P, SUPERHERO_SUPERPOWERS HP 
    WHERE P.id = HP.superpower_id AND HP.superhero_id = ?;
    """

    if not superhero_exists(id):
        return jsonify({"error": "Superhero not found."}), 404

    if request.method == "GET":
        return get_superhero_superpowers(query, id)

    body = json.loads(request.data)
    if not validate_id_body(body):
        return jsonify({"error": "Invalid superpower properties."}), 400

    if not superpower_exists(body["id"]):
        return jsonify({"error": "Superpower not found."}), 404

    select_query = """
    SELECT P.id
    FROM SUPERPOWERS P, SUPERHERO_SUPERPOWERS HP 
    WHERE P.id = HP.superpower_id AND HP.superhero_id = ? AND P.ID = ?;
    """
    superpower = get_db_data_by_value(select_query, [id, body["id"]])

    if superpower and "error" in superpower:
        return superpower, 500

    if request.method == "POST":
        return post_superhero_superpower(superpower, body, query, id)

    if request.method == "DELETE":
        return delete_superhero_superpower(superpower, body, id)
