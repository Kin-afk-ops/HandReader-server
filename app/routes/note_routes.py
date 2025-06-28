from flask import Blueprint, request, jsonify
from app.services.note_service import create_note_service, get_all_notes_service

note_routes = Blueprint("note_routes", __name__)

@note_routes.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    note = create_note_service(data['content'])
    return jsonify({"message": "Note created", "id": note.id})

@note_routes.route('/notes', methods=['GET'])
def get_notes():
    notes = get_all_notes_service()
    return jsonify([{"id": n.id, "content": n.content} for n in notes])
