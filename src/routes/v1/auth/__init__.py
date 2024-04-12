
"""
Endpoints for Users
"""

from flask import Blueprint, request
from .helpers import *
from flask_jwt_extended import jwt_required


blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")


@blueprint.route("/auth/token", methods=["POST"])
def users() -> dict:
    """Get the API token"""

    body = request.get_json()
    return get_token(body)


@blueprint.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> dict:
    """Refresh the API token"""

    return refresh_token()
