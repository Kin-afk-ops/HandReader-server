from flask import Blueprint, request, jsonify
from app.services.image_service import (
    create_image_service,
    get_all_images_service,
    get_image_by_id_service,
    update_image_service,
    delete_image_service,
    upload_image_cloudinary
)
import uuid

image_routes = Blueprint("image_routes", __name__)

@image_routes.route("/images", methods=["POST"])
def create_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        user_id = request.form.get("user_id")
        source = request.form.get("source", "upload")

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
       
        # 📌 GỌI HÀM Ở ĐÂY
        image_upload = upload_image_cloudinary(file)


        image = create_image_service(
            user_id=uuid.UUID(user_id),
            source=source,
            image_url=image_upload["image_url"],
            image_public_key=image_upload["public_key"]
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
