# app/routes/admin_action_routes.py
from flask import Blueprint, request, jsonify
from app.services.admin_action_service import (
    create_admin_action,
    get_all_admin_actions,
    get_admin_action_by_id,
    update_admin_action,
    delete_admin_action
)

admin_action_routes = Blueprint('admin_action_routes', __name__)

@admin_action_routes.route('/admin-actions', methods=['POST'])
def create():
    data = request.json
    return jsonify(create_admin_action(data)), 201

@admin_action_routes.route('/admin-actions', methods=['GET'])
def get_all():
    return jsonify(get_all_admin_actions())

@admin_action_routes.route('/admin-actions/<uuid:action_id>', methods=['GET'])
def get_one(action_id):
    result = get_admin_action_by_id(action_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Not found"}), 404

@admin_action_routes.route('/admin-actions/<uuid:action_id>', methods=['PUT'])
def update(action_id):
    data = request.json
    result = update_admin_action(action_id, data)
    if result:
        return jsonify(result)
    return jsonify({"error": "Not found"}), 404

@admin_action_routes.route('/admin-actions/<uuid:action_id>', methods=['DELETE'])
def delete(action_id):
    if delete_admin_action(action_id):
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404
