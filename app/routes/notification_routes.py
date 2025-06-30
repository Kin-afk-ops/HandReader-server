# app/routes/notification_routes.py
from flask import Blueprint, request, jsonify
from app.services.notification_service import (
    create_notification,
    get_all_notifications,
    get_notification_by_id,
    update_notification,
    delete_notification
)

notification_routes = Blueprint('notification_routes', __name__)

@notification_routes.route('/notifications', methods=['POST'])
def create():
    data = request.json
    notification = create_notification(data)
    return jsonify(notification), 201

@notification_routes.route('/notifications', methods=['GET'])
def get_all():
    return jsonify(get_all_notifications())

@notification_routes.route('/notifications/<uuid:notification_id>', methods=['GET'])
def get_one(notification_id):
    result = get_notification_by_id(notification_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Not found"}), 404

@notification_routes.route('/notifications/<uuid:notification_id>', methods=['PUT'])
def update(notification_id):
    data = request.json
    result = update_notification(notification_id, data)
    if result:
        return jsonify(result)
    return jsonify({"error": "Not found"}), 404

@notification_routes.route('/notifications/<uuid:notification_id>', methods=['DELETE'])
def delete(notification_id):
    if delete_notification(notification_id):
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404
