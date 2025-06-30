from flask import Blueprint, request, jsonify
from app.services.guide_service import *

guide_routes = Blueprint('guide_routes', __name__)

@guide_routes.route("/guides", methods=["POST"])
def create():
    data = request.get_json()
    guide = create_guide(data)
    return jsonify({"message": "Guide created", "id": str(guide.id)}), 201

@guide_routes.route("/guides", methods=["GET"])
def get_all():
    guides = get_all_guides()
    return jsonify([{"id": str(g.id), "title": g.title, "created_at": g.created_at.isoformat()} for g in guides]), 200

@guide_routes.route("/guides/<guide_id>", methods=["GET"])
def get_by_id(guide_id):
    guide = get_guide_by_id(guide_id)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify({"id": str(guide.id), "title": guide.title, "created_at": guide.created_at.isoformat()}), 200

@guide_routes.route("/guides/<guide_id>", methods=["PUT"])
def update(guide_id):
    data = request.get_json()
    guide = update_guide(guide_id, data)
    if not guide:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify({"message": "Guide updated"}), 200

@guide_routes.route("/guides/<guide_id>", methods=["DELETE"])
def delete(guide_id):
    success = delete_guide(guide_id)
    if not success:
        return jsonify({"error": "Guide not found"}), 404
    return jsonify({"message": "Guide deleted"}), 200
