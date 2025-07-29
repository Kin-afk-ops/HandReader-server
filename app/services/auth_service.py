from app import db
from app.models.admin_model import Admin
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

def login_auth_service(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return None, "Username and password are required"

    admin = Admin.query.filter_by(username=username).first()

    if not admin:
        return None, "Admin not found"

    if not check_password_hash(admin.password, password):
        return None, "Invalid password"
    additional_claims = {"role": admin.role}
    access_token = create_access_token(identity=str(admin.id), additional_claims=additional_claims)

    return {
        "access_token": access_token,
        "user_id": admin.id,
        "username": admin.username,
        "role": admin.role
    }, None



