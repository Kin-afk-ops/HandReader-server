import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class GuideStep(db.Model):
    __tablename__ = 'guide_steps'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guide_id = db.Column(UUID(as_uuid=True), db.ForeignKey('guides.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False, comment='Thứ tự bước')
    instruction_text = db.Column(db.Text, nullable=False, comment='Mô tả hành động cần làm')
    audio_url = db.Column(db.String, nullable=False, comment='Đường dẫn âm thanh hướng dẫn')
    expected_action = db.Column(db.String, nullable=False, comment='take_photo | read_result | repeat | confirm | ...')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    guide = db.relationship('Guide', backref=db.backref('steps', lazy=True, cascade="all, delete"))


    def to_dict(self):
        return {
            "id": str(self.id),
            "guide_id": str(self.guide_id),
            "step_number": self.step_number,
            "instruction_text": self.instruction_text,
            "audio_url": self.audio_url,
            "expected_action": self.expected_action,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }