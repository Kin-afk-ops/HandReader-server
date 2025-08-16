from app.models.feedback_model import Feedback
from app.models.image_model import Image
from app.models.recognition_result_model import RecognitionResult
from app.extensions import db
import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload
def create_feedback(data):
    feedback = Feedback(
        id=uuid.uuid4(),
        result_id=data["result_id"],
        user_id=data["user_id"],
        message=data["message"],
        status=data.get("status", "pending"),
        created_at=datetime.utcnow(),
        resolved_at=data.get("resolved_at")
    )
    db.session.add(feedback)
    db.session.commit()
    return feedback

def get_all_feedbacks():
    return Feedback.query.options(
        joinedload(Feedback.result).joinedload(RecognitionResult.image),  # dùng thuộc tính class-bound
        joinedload(Feedback.user)  # nếu muốn load user luôn
    ).all()

def get_feedback_by_id(feedback_id):
    return Feedback.query.get(feedback_id)


def get_feedback_stats_by_status():
    results = (
        db.session.query(Feedback.status, func.count(Feedback.id))
        .group_by(Feedback.status)
        .all()
    )
    return [{"type": status, "value": count} for status, count in results]

def update_feedback(feedback_id, data):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return None
    feedback.message = data.get("message", feedback.message)
    feedback.status = data.get("status", feedback.status)
    feedback.resolved_at = data.get("resolved_at", feedback.resolved_at)
    db.session.commit()
    return feedback

def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return False
    db.session.delete(feedback)
    db.session.commit()
    return True
