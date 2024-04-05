"""
Utils module for validations
"""


def body_is_valid(body: dict, is_superpower: bool = False) -> bool:
    """validate request body data"""

    if is_superpower and 'id' in body and len(body.keys()) == 1:
        return True
    if not is_superpower and 'name' in body and len(body.keys()) == 1:
        return True
    return False
