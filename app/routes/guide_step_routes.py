from flask import Blueprint, request, jsonify
from app.services.guide_step_service import *

guide_step_bp = Blueprint('guide_steps', __name__)

@guide_step_bp.route('/guide-steps', methods=['POST'])
def create():
    data = request.get_json()
    step = create_guide_step(data)
    return jsonify(step), 201

@guide_step_bp.route('/guide-steps', methods=['GET'])
def get_all():
    return jsonify(get_all_guide_steps())

@guide_step_bp.route('/guide-steps/<uuid:step_id>', methods=['GET'])
def get_by_id(step_id):
    step = get_guide_step_by_id(step_id)
    return jsonify(step) if step else (jsonify({'error': 'Not found'}), 404)

@guide_step_bp.route('/guide-steps/<uuid:step_id>', methods=['PUT'])
def update(step_id):
    data = request.get_json()
    step = update_guide_step(step_id, data)
    return jsonify(step) if step else (jsonify({'error': 'Not found'}), 404)

@guide_step_bp.route('/guide-steps/<uuid:step_id>', methods=['DELETE'])
def delete(step_id):
    success = delete_guide_step(step_id)
    return ('', 204) if success else (jsonify({'error': 'Not found'}), 404)
