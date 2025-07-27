# app/routes/history_routes.py
from flask import Blueprint, request, jsonify
from app.services.history_service import *

history_routes = Blueprint("history_routes", __name__)

@history_routes.route("/histories", methods=["POST"])
def create():
    data = request.get_json()
    history = create_history(data)
    return jsonify(history.to_dict()), 201

@history_routes.route("/getAll/histories", methods=["GET"])
def get_all():
    histories = get_all_histories()
    return jsonify([h.to_dict() for h in histories]), 200

@history_routes.route("/histories/id/<string:history_id>", methods=["GET"])
def get_by_id(history_id):
    history = get_history_by_id(history_id)
    if not history:
        return jsonify({"error": "Not found"}), 404
    return jsonify(history.to_dict()), 200

@history_routes.route("/histories/userId/<string:user_id>", methods=["GET"])
def get_by_userId(user_id):
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    histories = get_history_by_userId(user_id,offset,limit)


    histories_list = [h.to_dict() for h in histories]

    if not histories_list:
        return jsonify({"error": "Not found"}), 404
    return jsonify(histories_list), 200


@history_routes.route("/histories/save/<string:user_id>", methods=["GET"])
def get_by_save(user_id):
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    histories = get_history_by_save(user_id,offset,limit)
   


    histories_list = [h.to_dict() for h in histories]

    if not histories_list:
        return jsonify({"error": "Not found"}), 404
    return jsonify(histories_list), 200




@history_routes.route("/histories/saveLength/<string:user_id>", methods=["GET"])
def get_length_save_by_user_id(user_id):
    try:
        data = get_length_save(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_routes.route("/histories/length/<string:user_id>", methods=["GET"])
def get_length(user_id):
    try:
        data = get_length_history(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@history_routes.route("/histories/<string:history_id>", methods=["PUT"])
def update(history_id):
    data = request.get_json()
    history = update_history(history_id, data)
    if not history:
        return jsonify({"error": "Not found"}), 404
    return jsonify(history.to_dict()), 200

@history_routes.route("/histories/<string:history_id>", methods=["DELETE"])
def delete(history_id):
    if delete_history(history_id):
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404
