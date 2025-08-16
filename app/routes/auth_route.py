from flask import Blueprint, request, jsonify
from app.services.auth_service import login_auth_service,get_current_admin_info
from flask_jwt_extended import create_access_token,set_access_cookies,get_jwt_identity,get_jwt,unset_jwt_cookies,jwt_required

auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/login", methods=["POST"])
def auth_login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    result, error = login_auth_service(data)
    if error:
        return jsonify({"msg": error}), 401
    return result 




@auth_route.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)

def refresh():

    current_user = get_jwt_identity()
    
    # Bạn có thể lấy thêm thông tin role từ JWT claims nếu cần
    claims = get_jwt()
    role = claims.get("role", "user")  # hoặc mặc định là "user"

    new_access_token = create_access_token(identity=current_user, additional_claims={"role": role})
    
    resp = jsonify({"refresh": True, "msg": "Access token refreshed successfully"})
    set_access_cookies(resp, new_access_token)
    return resp, 200



@auth_route.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({"logout": True, "msg": "Tokens removed"})
    unset_jwt_cookies(resp)
    return resp, 200


@auth_route.route('/me')
@jwt_required()
def get_current_admin():
    admin_data = get_current_admin_info()
    if admin_data:
        return jsonify({"admin": admin_data})
    return jsonify({"msg": "admin not found"}), 404