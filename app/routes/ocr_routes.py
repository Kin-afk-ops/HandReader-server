from flask import Blueprint

ocr_bp = Blueprint("ocr", __name__)

@ocr_bp.route("/")
def hello():
    return "Hello from Flask + VietOCR project with Blueprint!"