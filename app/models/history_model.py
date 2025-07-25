# app/models/history_model.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class History(db.Model):
    __tablename__ = 'histories'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    result_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recognition_results.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('histories', lazy=True))
    result = db.relationship('RecognitionResult', backref=db.backref('histories', lazy=True))

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "result_id": str(self.result_id),
            "viewed_at": self.viewed_at.isoformat(),
            "recognized_text": self.result.recognized_text if self.result else None,
            "confidence": self.result.confidence if self.result else None,
            "is_saved_by_user": self.result.is_saved_by_user if self.result else None,
            "created_at": self.result.created_at.isoformat() if self.result and self.result.created_at else None
        }
