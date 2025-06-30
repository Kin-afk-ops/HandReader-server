from flask import Blueprint, request, jsonify
from app.services.guide_progress_service import *

guide_progress_bp = Blueprint('guide_progresses', __name__)

@guide_progress_bp.route('/guide-progresses', methods=['POST'])
def create():
    data = request.get_json()
    progress = create_guide_progress(data)
    return jsonify(progress), 201

@guide_progress_bp.route('/guide-progresses', methods=['GET'])
def get_all():
    return jsonify(get_all_guide_progresses())

@guide_progress_bp.route('/guide-progresses/<uuid:progress_id>', methods=['GET'])
def get_by_id(progress_id):
    progress = get_guide_progress_by_id(progress_id)
    return jsonify(progress) if progress else (jsonify({'error': 'Not found'}), 404)

@guide_progress_bp.route('/guide-progresses/<uuid:progress_id>', methods=['PUT'])
def update(progress_id):
    data = request.get_json()
    progress = update_guide_progress(progress_id, data)
    return jsonify(progress) if progress else (jsonify({'error': 'Not found'}), 404)

@guide_progress_bp.route('/guide-progresses/<uuid:progress_id>', methods=['DELETE'])
def delete(progress_id):
    success = delete_guide_progress(progress_id)
    return ('', 204) if success else (jsonify({'error': 'Not found'}), 404)
