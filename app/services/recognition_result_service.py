from app.models.recognition_result_model import RecognitionResult
from app.extensions import db
import uuid
from datetime import datetime

def create_recognition_result(data):
    new_result = RecognitionResult(
        id=uuid.uuid4(),
        image_id=data['image_id'],
        recognized_text=data['recognized_text'],
        confidence=data['confidence'],
        is_saved_by_user=data.get('is_saved_by_user', False),
        created_at=datetime.utcnow()
    )
    db.session.add(new_result)
    db.session.commit()
    return new_result

def get_all_results():
    return RecognitionResult.query.all()

def get_result_by_id(result_id):
    return RecognitionResult.query.get(result_id)

def update_result(result_id, data):
    result = RecognitionResult.query.get(result_id)
    if not result:
        return None
    result.recognized_text = data.get('recognized_text', result.recognized_text)
    result.confidence = data.get('confidence', result.confidence)
    result.is_saved_by_user = data.get('is_saved_by_user', result.is_saved_by_user)
    db.session.commit()
    return result

def delete_result(result_id):
    result = RecognitionResult.query.get(result_id)
    if not result:
        return None
    db.session.delete(result)
    db.session.commit()
    return result
