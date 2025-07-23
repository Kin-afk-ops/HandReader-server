import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    source = db.Column(db.String, nullable=False, comment='upload | camera | livestream')
    image_url = db.Column(db.String, nullable=False)
    image_public_key = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ ngược (nếu cần)
    user = db.relationship('User', backref=db.backref('images', lazy=True))
