from flask import Blueprint, request, jsonify
from app.services.user_service import create_user_service,update_user_service,delete_user_service,get_user_by_uid_service
from app.models.user_model import User

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = create_user_service(data)
        return jsonify({
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



from app.services.user_service import get_all_users_service

@user_routes.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = get_all_users_service()
        user_list = [{
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        } for user in users]

        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@user_routes.route("/users/<uuid:user_id>", methods=["GET"])
def get_users(user_id):
    try:
        user = get_user_by_uid_service(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        user_data = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@user_routes.route("/users/<uuid:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        updated_user = update_user_service(user_id, data)

        if not updated_user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": str(updated_user.id),
            "name": updated_user.name,
            "email": updated_user.email,
            "role": updated_user.role,
            "updated_at": updated_user.updated_at.isoformat() if updated_user.updated_at else None
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@user_routes.route("/users/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        success = delete_user_service(user_id)
        if not success:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
