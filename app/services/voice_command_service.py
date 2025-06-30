# app/services/voice_command_service.py
from app.models.voice_command_model import VoiceCommand
from app.extensions import db
import uuid
from datetime import datetime

def create_voice_command(data):
    command = VoiceCommand(
        id=uuid.uuid4(),
        user_id=data["user_id"],
        command_text=data["command_text"],
        action_trigger=data["action_trigger"],
        created_at=data.get("created_at", datetime.utcnow())
    )
    db.session.add(command)
    db.session.commit()
    return command

def get_all_voice_commands():
    return VoiceCommand.query.all()

def get_voice_command_by_id(command_id):
    return VoiceCommand.query.get(command_id)

def update_voice_command(command_id, data):
    command = VoiceCommand.query.get(command_id)
    if not command:
        return None
    command.command_text = data.get("command_text", command.command_text)
    command.action_trigger = data.get("action_trigger", command.action_trigger)
    db.session.commit()
    return command

def delete_voice_command(command_id):
    command = VoiceCommand.query.get(command_id)
    if not command:
        return False
    db.session.delete(command)
    db.session.commit()
    return True
