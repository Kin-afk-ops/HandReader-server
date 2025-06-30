import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class RecognitionResult(db.Model):
    __tablename__ = 'recognition_results'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = db.Column(UUID(as_uuid=True), db.ForeignKey('images.id'), nullable=False)
    recognized_text = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    is_saved_by_user = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    image = db.relationship("Image", backref=db.backref("recognition_results", lazy=True))