# app/routes/error_log_routes.py
from flask import Blueprint, request, jsonify
from app.services.error_log_service import (
    create_error_log,
    get_all_error_logs,
    get_error_log_by_id,
    update_error_log,
    delete_error_log
)

error_log_routes = Blueprint('error_log_routes', __name__)

@error_log_routes.route('/error-logs', methods=['POST'])
def create():
    data = request.json
    return jsonify(create_error_log(data)), 201

@error_log_routes.route('/error-logs', methods=['GET'])
def get_all():
    return jsonify(get_all_error_logs())

@error_log_routes.route('/error-logs/<uuid:log_id>', methods=['GET'])
def get_one(log_id):
    log = get_error_log_by_id(log_id)
    if log:
        return jsonify(log)
    return jsonify({"error": "Not found"}), 404

@error_log_routes.route('/error-logs/<uuid:log_id>', methods=['PUT'])
def update(log_id):
    data = request.json
    log = update_error_log(log_id, data)
    if log:
        return jsonify(log)
    return jsonify({"error": "Not found"}), 404

@error_log_routes.route('/error-logs/<uuid:log_id>', methods=['DELETE'])
def delete(log_id):
    if delete_error_log(log_id):
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404
