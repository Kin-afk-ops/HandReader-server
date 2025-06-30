# app/models/error_log_model.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class ErrorLog(db.Model):
    __tablename__ = 'error_logs'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    error_message = db.Column(db.Text, nullable=False)
    stack_trace = db.Column(db.Text, nullable=True)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('error_logs', lazy=True))

    def to_dict(self):  
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "error_message": self.error_message,
            "stack_trace": self.stack_trace,
            "occurred_at": self.occurred_at.isoformat()
        }
