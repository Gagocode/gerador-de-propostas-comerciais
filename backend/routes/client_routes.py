from flask import Blueprint, request, jsonify
from backend.services.client_service import ClientService

client_bp = Blueprint('clients', __name__)
service = ClientService()


@client_bp.route('/clientes', methods=['GET'])
def list_clients():
    return jsonify(service.list_all()), 200


@client_bp.route('/clientes/<int:client_id>', methods=['GET'])
def get_client(client_id):
    result, error = service.get(client_id)
    if error:
        return jsonify({'erro': error}), 404
    return jsonify(result), 200


@client_bp.route('/clientes', methods=['POST'])
def create_client():
    data = request.get_json(force=True)
    result, error = service.create(data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 201


@client_bp.route('/clientes/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.get_json(force=True)
    result, error = service.update(client_id, data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 200
