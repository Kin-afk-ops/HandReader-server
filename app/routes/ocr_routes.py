from flask import Blueprint, request, jsonify
from app.utils.helpers import base64_to_image
from app.services.vietocr_service import predict_text_from_image

ocr_bp = Blueprint("ocr", __name__)

@ocr_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        base64_img = data.get("image")

        if not base64_img:
            return jsonify({"error": "No image provided"}), 400

        image = base64_to_image(base64_img)
        result_text = predict_text_from_image(image)

        return jsonify({"text": result_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
