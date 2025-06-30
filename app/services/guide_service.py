from app.models.guide_model import Guide
from app.extensions import db
import uuid
from datetime import datetime

def create_guide(data):
    guide = Guide(
        id=uuid.uuid4(),
        title=data["title"],
        created_at=datetime.utcnow()
    )
    db.session.add(guide)
    db.session.commit()
    return guide

def get_all_guides():
    return Guide.query.all()

def get_guide_by_id(guide_id):
    return Guide.query.get(guide_id)

def update_guide(guide_id, data):
    guide = Guide.query.get(guide_id)
    if not guide:
        return None
    guide.title = data.get("title", guide.title)
    db.session.commit()
    return guide

def delete_guide(guide_id):
    guide = Guide.query.get(guide_id)
    if not guide:
        return False
    db.session.delete(guide)
    db.session.commit()
    return True
