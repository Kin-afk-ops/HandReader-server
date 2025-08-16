from flask import Flask, jsonify, request
from app import db
from app.models.admin_model import Admin
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,set_access_cookies,create_refresh_token,set_refresh_cookies,get_jwt_identity

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
    refresh_token = create_refresh_token(identity=str(admin.id), additional_claims=additional_claims)
   
    resp = jsonify({
        "id": admin.id,
        "username": admin.username,
        "role": admin.role
    })
    set_access_cookies(resp, access_token, max_age=60 * 60 * 24 * 7)
    set_refresh_cookies(resp, refresh_token)

    return resp, None




def get_current_admin_info():
    admin_id = get_jwt_identity()
    admin = Admin.query.get(admin_id)
    if admin:
        return {
            "id": admin.id,
            "name": admin.username
        }
    return None