import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True, comment='Có thể null nếu không đăng nhập bằng email')
    password = db.Column(db.String, nullable=True, comment='Chỉ cần cho admin/super_admin')
    role = db.Column(db.String, nullable=False, comment='user | admin | super_admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
