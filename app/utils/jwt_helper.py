from flask_jwt_extended import get_jwt_identity

def require_roles(*roles):
    identity = get_jwt_identity()
    if identity["role"] not in roles:
        return False, identity
    return True, identity
