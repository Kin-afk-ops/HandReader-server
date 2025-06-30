# app/routes/voice_command_routes.py
from flask import Blueprint, request, jsonify
from app.services.voice_command_service import *

voice_command_routes = Blueprint("voice_command_routes", __name__)

@voice_command_routes.route("/voice-commands", methods=["POST"])
def create():
    data = request.get_json()
    command = create_voice_command(data)
    return jsonify(command.to_dict()), 201

@voice_command_routes.route("/voice-commands", methods=["GET"])
def get_all():
    commands = get_all_voice_commands()
    return jsonify([cmd.to_dict() for cmd in commands]), 200

@voice_command_routes.route("/voice-commands/<string:command_id>", methods=["GET"])
def get_by_id(command_id):
    command = get_voice_command_by_id(command_id)
    if not command:
        return jsonify({"error": "Not found"}), 404
    return jsonify(command.to_dict()), 200

@voice_command_routes.route("/voice-commands/<string:command_id>", methods=["PUT"])
def update(command_id):
    data = request.get_json()
    command = update_voice_command(command_id, data)
    if not command:
        return jsonify({"error": "Not found"}), 404
    return jsonify(command.to_dict()), 200

@voice_command_routes.route("/voice-commands/<string:command_id>", methods=["DELETE"])
def delete(command_id):
    if delete_voice_command(command_id):
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404
