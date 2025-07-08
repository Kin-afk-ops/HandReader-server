from flask import Blueprint, request, jsonify
from app.services.auth_service import login_auth_service

auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/login", methods=["POST"])
def auth_login():

    data = request.get_json()
    result, error = login_auth_service(data)
    if error:
        return jsonify({"msg": error}), 401
    return jsonify(result), 200
 



