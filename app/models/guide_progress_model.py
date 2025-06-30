import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class GuideProgress(db.Model):
    __tablename__ = 'guide_progresses'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    guide_id = db.Column(UUID(as_uuid=True), db.ForeignKey('guides.id'), nullable=False)
    current_step = db.Column(db.Integer, nullable=False, comment='Bước hiện tại')
    is_completed = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('guide_progresses', lazy=True))
    guide = db.relationship('Guide', backref=db.backref('progresses', lazy=True, cascade="all, delete"))
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "guide_id": str(self.guide_id),
            "current_step": self.current_step,
            "is_completed": self.is_completed,
            "last_updated": self.last_updated.isoformat()
        }


    
