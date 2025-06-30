import uuid
from datetime import datetime
from app.extensions import db
from app.models.guide_step_model import GuideStep

def create_guide_step(data):
    step = GuideStep(
        id=uuid.uuid4(),
        guide_id=data["guide_id"],
        step_number=data["step_number"],
        instruction_text=data["instruction_text"],
        audio_url=data["audio_url"],
        expected_action=data["expected_action"],
        created_at=datetime.utcnow()
    )
    db.session.add(step)
    db.session.commit()
    return step.to_dict()

def get_all_guide_steps():
    return GuideStep.query.all()

def get_guide_step_by_id(step_id):
    return GuideStep.query.get(step_id)

def update_guide_step(step_id, data):
    step = GuideStep.query.get(step_id)
    if not step:
        return None

    step.step_number = data.get("step_number", step.step_number)
    step.instruction_text = data.get("instruction_text", step.instruction_text)
    step.audio_url = data.get("audio_url", step.audio_url)
    step.expected_action = data.get("expected_action", step.expected_action)
    db.session.commit()
    return step

def delete_guide_step(step_id):
    step = GuideStep.query.get(step_id)
    if not step:
        return False
    db.session.delete(step)
    db.session.commit()
    return True
