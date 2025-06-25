from flask import Flask
from flask_cors import CORS , cross_origin


from flask import Flask

# Khoi tao flask server

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config["CORS_HEADERS"] = "Content-Type"
    # Register các blueprint
    from app.routes.ocr_routes import ocr_bp
    app.register_blueprint(ocr_bp)
    return app



