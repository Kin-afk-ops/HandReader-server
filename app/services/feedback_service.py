from app.models.feedback_model import Feedback
from app.extensions import db
import uuid
from datetime import datetime

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
    return Feedback.query.all()

def get_feedback_by_id(feedback_id):
    return Feedback.query.get(feedback_id)

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
