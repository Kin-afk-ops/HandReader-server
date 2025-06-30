from flask import Blueprint, request, jsonify
from app.services.image_service import (
    create_image_service,
    get_all_images_service,
    get_image_by_id_service,
    update_image_service,
    delete_image_service,
)
import uuid

image_routes = Blueprint("image_routes", __name__)

@image_routes.route("/images", methods=["POST"])
def create_image():
    data = request.get_json()
    try:
        image = create_image_service(
            user_id=uuid.UUID(data["user_id"]),
            source=data["source"],
            image_url=data["image_url"]
        )
        return jsonify({"id": str(image.id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@image_routes.route("/images", methods=["GET"])
def get_all_images():
    images = get_all_images_service()
    return jsonify([
        {
            "id": str(img.id),
            "user_id": str(img.user_id),
            "source": img.source,
            "image_url": img.image_url,
            "created_at": img.created_at.isoformat()
        }
        for img in images
    ])

@image_routes.route("/images/<uuid:image_id>", methods=["GET"])
def get_image_by_id(image_id):
    img = get_image_by_id_service(image_id)
    if not img:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": str(img.id),
        "user_id": str(img.user_id),
        "source": img.source,
        "image_url": img.image_url,
        "created_at": img.created_at.isoformat()
    })

@image_routes.route("/images/<uuid:image_id>", methods=["PUT"])
def update_image(image_id):
    data = request.get_json()
    img = update_image_service(image_id, data)
    if not img:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Updated"})

@image_routes.route("/images/<uuid:image_id>", methods=["DELETE"])
def delete_image(image_id):
    img = delete_image_service(image_id)
    if not img:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})
