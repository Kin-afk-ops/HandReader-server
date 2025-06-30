# app/services/history_service.py
from app.models.history_model import History
from app.extensions import db
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
