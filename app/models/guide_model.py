import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Guide(db.Model):
    __tablename__ = 'guides'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False, comment="Tên của hướng dẫn")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
