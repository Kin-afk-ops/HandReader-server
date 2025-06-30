# app/models/voice_command_model.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class VoiceCommand(db.Model):
    __tablename__ = 'voice_commands'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    command_text = db.Column(db.String, nullable=False, comment="Câu lệnh người dùng nói")
    action_trigger = db.Column(db.String, nullable=False, comment="take_photo | read_result | repeat | go_back | open_history | ...")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("voice_commands", lazy=True))

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "command_text": self.command_text,
            "action_trigger": self.action_trigger,
            "created_at": self.created_at.isoformat()
        }
