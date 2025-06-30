# app/models/admin_action_model.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class AdminAction(db.Model):
    __tablename__ = 'admin_actions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String, nullable=False, comment='create_user | delete_user | resolve_feedback | etc.')
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('User', backref=db.backref('admin_actions', lazy=True))

    def to_dict(self):
        return {
            "id": str(self.id),
            "admin_id": str(self.admin_id),
            "action_type": self.action_type,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
