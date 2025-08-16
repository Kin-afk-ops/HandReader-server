from flask import Blueprint, request, jsonify
from app.services.feedback_service import *
from app.utils.jwt_helper import require_roles,require_admin_or_super_admin,require_super_admin

feedback_routes = Blueprint("feedback_routes", __name__)

@feedback_routes.route("/feedbacks", methods=["POST"])
def create():
    data = request.get_json()
    feedback = create_feedback(data)
    return jsonify({"id": str(feedback.id)}), 201

@feedback_routes.route("/feedbacks/all", methods=["GET"])
def get_all():
    feedbacks = get_all_feedbacks()
    return jsonify([
        {
            "id": str(f.id),
            "user_id": str(f.user_id),
            "message": f.message,
            "status": f.status,
            "created_at": f.created_at.isoformat(),
            "resolved_at": f.resolved_at.isoformat() if f.resolved_at else None,
            "result": {
                "id": str(f.result.id),
                "recognized_text": f.result.recognized_text,
                "confidence": f.result.confidence,
                "is_saved_by_user": f.result.is_saved_by_user,
                "created_at": f.result.created_at.isoformat(),
                "image": {
                    "id": str(f.result.image.id),
                    "image_url": f.result.image.image_url,
                    "image_public_key": f.result.image.image_public_key,
                    "source": f.result.image.source,
                    "created_at": f.result.image.created_at.isoformat(),
                },
            },
        }
        for f in feedbacks
    ])

@feedback_routes.route("/feedback/stats-by-type", methods=["GET"])
@require_admin_or_super_admin()
def feedback_stats_by_status():
    data = get_feedback_stats_by_status()
    return jsonify(data), 200


@feedback_routes.route("/feedbacks/info/<uuid:feedback_id>", methods=["GET"])
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
