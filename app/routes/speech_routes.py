# speech.py

from flask import Blueprint, request, send_file, jsonify
import openai
from io import BytesIO
import os

speech_route = Blueprint("speech", __name__)

# Thiết lập API key từ biến môi trường (hoặc thay thế trực tiếp nếu cần)
openai.api_key = os.getenv("OPENAI_API_KEY")

@speech_route.route("/speech", methods=["POST"])
def generate_speech():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    try:
        response = openai.audio.speech.create(
            model="tts-1",
            input=text,
            voice="nova",  # hoặc shimmer, alloy...
            response_format="mp3"
        )

        audio_bytes = BytesIO(response.read())
        audio_bytes.seek(0)

        return send_file(
            audio_bytes,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech.mp3"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
