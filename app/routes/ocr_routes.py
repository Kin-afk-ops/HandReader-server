from flask import Blueprint, request, jsonify
from app.utils.helpers import base64_to_image
from app.services.vietocr_service import predict_text_from_image, split_lines_from_image

ocr_bp = Blueprint("ocr", __name__)

@ocr_bp.route("/predict-paragraph", methods=["POST"])
def predict_paragraph():
    try:
        data = request.get_json()
        base64_img = data.get("image")

        if not base64_img:
            return jsonify({"error": "No image provided"}), 400

        image = base64_to_image(base64_img)
        line_images = split_lines_from_image(image)
        print(f"[DEBUG] Tách được {len(line_images)} dòng")

        full_text = ""
        for line_img in line_images:
            result = predict_text_from_image(line_img)
            full_text += result.strip() + "\n"

        return jsonify({"text": full_text.strip()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ocr_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("✅ JSON nhận được")

        base64_img = data.get("image")
        if not base64_img:
            print("❌ Không có ảnh được gửi")
            return jsonify({"error": "No image provided"}), 400

        image = base64_to_image(base64_img)
        print("✅ Chuyển base64 thành ảnh xong")

        print("⏳ Đang nhận diện văn bản...")
        result_text = predict_text_from_image(image)

        print("✅ Kết quả:", result_text)
        return jsonify({"text": result_text}), 200

    except Exception as e:
        print("🔥 Lỗi:", str(e))
        return jsonify({"error": str(e)}), 500
