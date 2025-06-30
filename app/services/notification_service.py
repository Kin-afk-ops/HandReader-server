# app/services/notification_service.py
from app.models.notification_model import Notification
from app.extensions import db
import uuid
from datetime import datetime

def create_notification(data):
    notification = Notification(
        id=uuid.uuid4(),
        user_id=data["user_id"],
        message=data["message"],
        is_read=data.get("is_read", False),
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()
    return notification.to_dict()

def get_all_notifications():
    return [n.to_dict() for n in Notification.query.all()]

def get_notification_by_id(notification_id):
    notif = Notification.query.get(notification_id)
    return notif.to_dict() if notif else None

def update_notification(notification_id, data):
    notif = Notification.query.get(notification_id)
    if not notif:
        return None
    notif.message = data.get("message", notif.message)
    notif.is_read = data.get("is_read", notif.is_read)
    db.session.commit()
    return notif.to_dict()

def delete_notification(notification_id):
    notif = Notification.query.get(notification_id)
    if not notif:
        return False
    db.session.delete(notif)
    db.session.commit()
    return True
