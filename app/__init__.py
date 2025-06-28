import os
from flask import Flask
from flask_cors import CORS , cross_origin
from app.models.user_model import User  # ✅ Import model ở đây
from app.models.note_model import Note
from dotenv import load_dotenv


from flask import Flask

# Khoi tao flask server
from app.extensions import db  

def create_app():
    app = Flask(__name__)

    CORS(app)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{int(os.getenv('DB_PORT', 5432))}/{os.getenv('DB_NAME')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) 

      # ✅ Phải đặt sau khi init_app và import model
    with app.app_context():
        db.create_all()

    app.config["CORS_HEADERS"] = "Content-Type"
    # Register các blueprint
    from app.routes.ocr_routes import ocr_bp
    from app.routes.db_routes import db_routes
    from app.routes.note_routes import note_routes
    from app.routes.user_routes import user_routes


    app.register_blueprint(ocr_bp)
    app.register_blueprint(db_routes)
    app.register_blueprint(note_routes)
    app.register_blueprint(user_routes)
    return app



