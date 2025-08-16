from flask import Blueprint, request, jsonify
from app.services.admin_service import create_admin_service,update_admin_password_service,get_all_admins_service,delete_admin_service
from app.utils.jwt_helper import require_roles,require_admin_or_super_admin,require_super_admin

admin_route = Blueprint("admin_route", __name__)

@admin_route.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "admin")

    response, status_code = create_admin_service(username, password, role)
    return jsonify(response), status_code


@admin_route.route('/admins/<uuid:admin_id>', methods=['PUT'])
@require_admin_or_super_admin()
def update_admin_password(admin_id):
    data = request.get_json()
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    response, status_code = update_admin_password_service(admin_id, current_password, new_password)
    return jsonify(response), status_code


@admin_route.route('/admins', methods=['GET'])
@require_super_admin()  # chỉ super_admin được xem danh sách admin
def get_all_admins():
    admins = get_all_admins_service()
    return jsonify(admins), 200

@admin_route.route('/admins/<uuid:admin_id>', methods=['DELETE'])

def delete_admin(admin_id):
    response, status_code = delete_admin_service(admin_id)
    return jsonify(response), status_code