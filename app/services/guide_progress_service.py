import uuid
from datetime import datetime
from app.extensions import db
from app.models.guide_progress_model import GuideProgress

def create_guide_progress(data):
    progress = GuideProgress(
        id=uuid.uuid4(),
        user_id=data["user_id"],
        guide_id=data["guide_id"],
        current_step=data["current_step"],
        is_completed=data.get("is_completed", False),
        last_updated=datetime.utcnow()
    )
    db.session.add(progress)
    db.session.commit()
    return progress.to_dict()

def get_all_guide_progresses():
    return GuideProgress.query.all()

def get_guide_progress_by_id(progress_id):
    return GuideProgress.query.get(progress_id)

def update_guide_progress(progress_id, data):
    progress = GuideProgress.query.get(progress_id)
    if not progress:
        return None

    progress.current_step = data.get("current_step", progress.current_step)
    progress.is_completed = data.get("is_completed", progress.is_completed)
    progress.last_updated = datetime.utcnow()

    db.session.commit()
    return progress

def delete_guide_progress(progress_id):
    progress = GuideProgress.query.get(progress_id)
    if not progress:
        return False

    db.session.delete(progress)
    db.session.commit()
    return True
