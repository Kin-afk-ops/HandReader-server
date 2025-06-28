from flask import Blueprint, request, jsonify
from app.services.user_service import create_user_service
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
