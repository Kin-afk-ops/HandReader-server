from flask import Blueprint, request, jsonify
from app.services.feedback_service import *

feedback_routes = Blueprint("feedback_routes", __name__)

@feedback_routes.route("/feedbacks", methods=["POST"])
def create():
    data = request.get_json()
    feedback = create_feedback(data)
    return jsonify({"id": str(feedback.id)}), 201

@feedback_routes.route("/feedbacks", methods=["GET"])
def get_all():
    feedbacks = get_all_feedbacks()
    return jsonify([
        {
            "id": str(f.id),
            "user_id": str(f.user_id),
            "result_id": str(f.result_id),
            "message": f.message,
            "status": f.status,
            "created_at": f.created_at.isoformat(),
            "resolved_at": f.resolved_at.isoformat() if f.resolved_at else None
        }
        for f in feedbacks
    ])

@feedback_routes.route("/feedbacks/<uuid:feedback_id>", methods=["GET"])
def get_one(feedback_id):
    feedback = get_feedback_by_id(feedback_id)
    if not feedback:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": str(feedback.id),
        "user_id": str(feedback.user_id),
        "result_id": str(feedback.result_id),
        "message": feedback.message,
        "status": feedback.status,
        "created_at": feedback.created_at.isoformat(),
        "resolved_at": feedback.resolved_at.isoformat() if feedback.resolved_at else None
    })

@feedback_routes.route("/feedbacks/<uuid:feedback_id>", methods=["PUT"])
def update(feedback_id):
    data = request.get_json()
    feedback = update_feedback(feedback_id, data)
    if not feedback:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Updated successfully"})

@feedback_routes.route("/feedbacks/<uuid:feedback_id>", methods=["DELETE"])
def delete(feedback_id):
    success = delete_feedback(feedback_id)
    if not success:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted successfully"})
