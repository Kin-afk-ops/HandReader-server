from flask import Blueprint, request, jsonify
from app.services import recognition_result_service
from app.models.recognition_result_model import RecognitionResult
from app.extensions import db

recognition_result_bp = Blueprint('recognition_result', __name__, url_prefix="/recognition-results")

@recognition_result_bp.route("/", methods=["POST"])
def create_result():
    data = request.get_json()
    result = recognition_result_service.create_recognition_result(data)
    return jsonify({"id": str(result.id)}), 201

@recognition_result_bp.route("/", methods=["GET"])
def list_results():
    results = recognition_result_service.get_all_results()
    return jsonify([
        {
            "id": str(r.id),
            "image_id": str(r.image_id),
            "recognized_text": r.recognized_text,
            "confidence": r.confidence,
            "is_saved_by_user": r.is_saved_by_user,
            "created_at": r.created_at.isoformat()
        } for r in results
    ])

@recognition_result_bp.route("/<uuid:result_id>", methods=["GET"])
def get_result(result_id):
    result = recognition_result_service.get_result_by_id(result_id)
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": str(result.id),
        "image_id": str(result.image_id),
        "recognized_text": result.recognized_text,
        "confidence": result.confidence,
        "is_saved_by_user": result.is_saved_by_user,
        "created_at": result.created_at.isoformat()
    })

@recognition_result_bp.route("/<uuid:result_id>", methods=["PUT"])
def update_result(result_id):
    data = request.get_json()
    result = recognition_result_service.update_result(result_id, data)
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Updated successfully"})

@recognition_result_bp.route("/<uuid:result_id>", methods=["DELETE"])
def delete_result(result_id):
    result = recognition_result_service.delete_result(result_id)
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted successfully"})
