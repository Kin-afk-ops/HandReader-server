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

def get_all_feedback_service():
    feedbacks = (
        Feedback.query.options(
            joinedload(Feedback.result).joinedload(RecognitionResult.image)  # load result + image luôn
        )
        .order_by(Feedback.created_at.desc())
        .all()
    )

    result = []
    for fb in feedbacks:
        r = fb.result
        img = r.image if r else None

        result.append({
            # --- Trường từ Feedback ---
            "feedback_id": str(fb.id),
            "user_id": str(fb.user_id),
            "message": fb.message,
            "status": fb.status,
            "created_at": fb.created_at.isoformat(),
            "resolved_at": fb.resolved_at.isoformat() if fb.resolved_at else None,

            # --- Trường từ RecognitionResult ---
            **({
                "result_id": str(r.id),
                "recognized_text": r.recognized_text,
                "confidence": r.confidence,
                "is_saved_by_user": r.is_saved_by_user,
                "result_created_at": r.created_at.isoformat(),
            } if r else {}),

            # --- Trường từ Image ---
            **({
                "image_id": str(img.id),
                "image_url": img.image_url,
                "image_public_key": img.image_public_key,
                "source": img.source,
                "image_created_at": img.created_at.isoformat(),
            } if img else {})
        })

    return result

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
