import os
from flask import Flask
from flask_cors import CORS , cross_origin
from flask_jwt_extended import JWTManager
from app.models.user_model import User
from app.models.recognition_result_model import RecognitionResult  
from app.models.image_model import Image  
from app.models.note_model import Note
from app.models.feedback_model import Feedback
from app.models.notification_model import Notification
from app.models.admin_action_model import AdminAction
from app.models.error_log_model import ErrorLog
from app.models.guide_model import Guide
from app.models.guide_step_model import GuideStep
from app.models.guide_progress_model import GuideProgress
from app.models.history_model import History
from app.models.voice_command_model import VoiceCommand
from dotenv import load_dotenv
import cloudinary


from flask import Flask


# Khoi tao flask server
from app.extensions import db  

# Khoi tao jwt 
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    CORS(app)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{int(os.getenv('DB_PORT', 5432))}/{os.getenv('DB_NAME')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key") 



    
    jwt.init_app(app)
    db.init_app(app) 


   

      # ✅ Phải đặt sau khi init_app và import model
    with app.app_context():
        # db.drop_all()
        db.create_all()

    app.config["CORS_HEADERS"] = "Content-Type"
    # Register các blueprint
    from app.routes.ocr_routes import ocr_bp
    from app.routes.db_routes import db_routes
    from app.routes.note_routes import note_routes
    from app.routes.user_routes import user_routes
    from app.routes.image_routes import image_routes
    from app.routes.recognition_result_routes import recognition_result_bp
    from app.routes.feedback_routes import feedback_routes
    from app.routes.notification_routes import notification_routes
    from app.routes.admin_action_routes import admin_action_routes
    from app.routes.error_log_routes import error_log_routes
    from app.routes.guide_routes import guide_routes
    from app.routes.guide_step_routes import guide_step_bp
    from app.routes.guide_progress_routes import guide_progress_bp
    from app.routes.history_routes import history_routes
    from app.routes.voice_command_routes import voice_command_routes
    from app.routes.auth_route import auth_route
    # from app.routes.speech_routes import speech_route






    app.register_blueprint(ocr_bp)
    app.register_blueprint(db_routes)
    app.register_blueprint(note_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(recognition_result_bp)
    app.register_blueprint(image_routes)
    app.register_blueprint(feedback_routes)
    app.register_blueprint(notification_routes)
    app.register_blueprint(admin_action_routes)
    app.register_blueprint(error_log_routes)
    app.register_blueprint(guide_routes)
    app.register_blueprint(guide_step_bp)
    app.register_blueprint(guide_progress_bp)
    app.register_blueprint(history_routes)
    app.register_blueprint(voice_command_routes)
    app.register_blueprint(auth_route)
    # app.register_blueprint(speech_route)

    return app



