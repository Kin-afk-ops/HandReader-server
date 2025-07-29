from flask import Blueprint, request, jsonify
from app.services.admin_service import create_admin_service

admin_route = Blueprint("admin_route", __name__)

@admin_route.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "admin")

    response, status_code = create_admin_service(username, password, role)
    return jsonify(response), status_code
