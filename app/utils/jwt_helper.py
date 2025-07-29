from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from flask import jsonify
def require_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            print(f"[DEBUG] Required roles: {roles}")

            claims = get_jwt()
            print(f"[DEBUG] JWT Claims: {claims}")

            user_role = claims.get("role")
            print(f"[DEBUG] User role from JWT: {user_role}")

            if user_role not in roles:
                print("[DEBUG] Permission denied: role not in allowed roles")
                return jsonify({"msg": "Permission denied"}), 403

            print("[DEBUG] Permission granted")
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_admin_or_super_admin():
    return require_roles("admin", "super_admin")

def require_super_admin():
    return require_roles("super_admin")