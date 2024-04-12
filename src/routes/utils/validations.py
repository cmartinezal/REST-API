"""
Utils module for validations
"""


def validate_name_body(body: dict) -> bool:
    """validate superhero body data"""

    if "name" in body and len(body.keys()) == 1:
        return True
    return False


def validate_id_body(body: dict) -> bool:
    """validate superpower body data"""

    if "id" in body and len(body.keys()) == 1:
        return True
    return False


def validate_user_body(body: dict) -> bool:
    """validate user body data"""

    if len(body.keys()) != 4:
        return False

    if "email" not in body:
        return False

    if "first_name" not in body:
        return False

    if "last_name" not in body:
        return False

    if "password" not in body:
        return False

    return True
