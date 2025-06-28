from app.models.note_model import Note, db

def create_note_service(content):
    note = Note(content=content)
    db.session.add(note)
    db.session.commit()
    return note

def get_all_notes_service():
    return Note.query.all()
