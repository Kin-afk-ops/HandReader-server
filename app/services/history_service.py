# app/services/history_service.py
from app.models.history_model import History
from app.models.recognition_result_model import RecognitionResult
from app.extensions import db
from sqlalchemy import func
import uuid
from datetime import datetime

def create_history(data):
    history = History(
        id=uuid.uuid4(),
        user_id=data["user_id"],
        result_id=data["result_id"],
        viewed_at=data.get("viewed_at", datetime.utcnow())
    )
    db.session.add(history)
    db.session.commit()
    return history

def get_all_histories():
    return History.query.all()

def get_history_by_id(history_id):
    return History.query.get(history_id)


def get_history_by_userId(user_id, offset, limit):
    histories = (
        db.session.query(History)
        .join(RecognitionResult, History.result_id == RecognitionResult.id)
        .filter(History.user_id == user_id)
        .order_by(History.viewed_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return histories


def get_history_by_save(user_id, offset, limit):
    histories = (
         db.session.query(History)
        .join(RecognitionResult, History.result_id == RecognitionResult.id)
        .filter(History.user_id == user_id)
        .filter(RecognitionResult.is_saved_by_user == True)
        .order_by(History.viewed_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return histories


def get_length_history(user_id):
    total = db.session.query(func.count(History.id)).filter_by(user_id=user_id).scalar()
    return {
        "total": total,
   }
   

def get_length_save(user_id):
    total = (
        db.session.query(func.count(History.id))
        .join(RecognitionResult, History.result_id == RecognitionResult.id)
        .filter(History.user_id == user_id)
        .filter(RecognitionResult.is_saved_by_user == True)
        .scalar()
    )
    return {
        "total": total,
   }
   




def update_history(history_id, data):
    history = History.query.get(history_id)
    if not history:
        return None
    history.viewed_at = data.get("viewed_at", history.viewed_at)
    db.session.commit()
    return history

def delete_history(history_id):
    history = History.query.get(history_id)
    if not history:
        return False
    db.session.delete(history)
    db.session.commit()
    return True
