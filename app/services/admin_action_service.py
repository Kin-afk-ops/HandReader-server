# app/services/admin_action_service.py
from app.models.admin_action_model import AdminAction
from app.extensions import db
import uuid
from datetime import datetime

def create_admin_action(data):
    action = AdminAction(
        id=uuid.uuid4(),
        admin_id=data["admin_id"],
        action_type=data["action_type"],
        details=data.get("details"),
        timestamp=datetime.utcnow()
    )
    db.session.add(action)
    db.session.commit()
    return action.to_dict()

def get_all_admin_actions():
    return [a.to_dict() for a in AdminAction.query.all()]

def get_admin_action_by_id(action_id):
    a = AdminAction.query.get(action_id)
    return a.to_dict() if a else None

def update_admin_action(action_id, data):
    action = AdminAction.query.get(action_id)
    if not action:
        return None
    action.action_type = data.get("action_type", action.action_type)
    action.details = data.get("details", action.details)
    db.session.commit()
    return action.to_dict()

def delete_admin_action(action_id):
    action = AdminAction.query.get(action_id)
    if not action:
        return False
    db.session.delete(action)
    db.session.commit()
    return True
