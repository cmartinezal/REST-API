"""
Helper functions for Users
"""

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from flask import jsonify
from ...utils.database import get_db_data_by_value


def get_token(auth: dict) -> dict:
    """Get the API token for a existing user"""

    if not auth:
        return jsonify({"error": "Forbidden"}), 403

    user = get_db_data_by_value(
        "SELECT id, email, password FROM USERS WHERE email = ?", [auth["email"],])

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    user_password = user[0]["password"]

    if auth and check_password_hash(user_password, auth.get("password", "")):
        access_token = create_access_token(identity=user[0]["id"], fresh=True)
        refresh_token = create_refresh_token(user[0]["id"])

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

    return jsonify({"error": "Unauthorized"}), 401


def refresh_token() -> None:
    """Refresh the API token using an access_token"""

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
