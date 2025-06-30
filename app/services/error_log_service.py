# app/services/error_log_service.py
from app.models.error_log_model import ErrorLog
from app.extensions import db
import uuid
from datetime import datetime

def create_error_log(data):
    log = ErrorLog(
        id=uuid.uuid4(),
        user_id=data["user_id"],
        error_message=data["error_message"],
        stack_trace=data.get("stack_trace"),
        occurred_at=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
    return log.to_dict()

def get_all_error_logs():
    return [log.to_dict() for log in ErrorLog.query.all()]

def get_error_log_by_id(log_id):
    log = ErrorLog.query.get(log_id)
    return log.to_dict() if log else None

def update_error_log(log_id, data):
    log = ErrorLog.query.get(log_id)
    if not log:
        return None
    log.error_message = data.get("error_message", log.error_message)
    log.stack_trace = data.get("stack_trace", log.stack_trace)
    db.session.commit()
    return log.to_dict()

def delete_error_log(log_id):
    log = ErrorLog.query.get(log_id)
    if not log:
        return False
    db.session.delete(log)
    db.session.commit()
    return True
