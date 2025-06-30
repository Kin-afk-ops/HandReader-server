import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    result_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recognition_results.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    result = db.relationship('RecognitionResult', backref=db.backref('feedbacks', lazy=True))
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
