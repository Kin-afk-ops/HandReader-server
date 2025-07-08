from app import db
from app.models.user_model import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

def login_auth_service(data):
    name = data.get("name")
    password = data.get("password", None)  

    if not name:
        return None, "Missing 'name'"
    user = User.query.filter_by(name=name).first()

    if user.role == "user":
        # Không cần password
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return {
            "access_token": access_token,
            "user_id": user.id,
            "name": user.name,
            "role": user.role
        }, None

    elif user.role in ["admin", "super_admin"]:
        if not password:
            return None, "Password required for admin"
        if not check_password_hash(user.password, password):
            return None, "Invalid password"
        
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return {
            "access_token": access_token,
            "user_id": user.id,
            "name": user.name,
            "role": user.role
        }, None

    else:
        return None, f"Unknown role '{user.role}'"

