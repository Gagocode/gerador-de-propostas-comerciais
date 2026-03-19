from flask import Blueprint, request, jsonify
from backend.services.service_service import ServiceService

service_bp = Blueprint('services', __name__)
service = ServiceService()


@service_bp.route('/servicos', methods=['GET'])
def list_services():
    return jsonify(service.list_all()), 200


@service_bp.route('/servicos', methods=['POST'])
def create_service():
    data = request.get_json(force=True)
    result, error = service.create(data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 201


@service_bp.route('/servicos/<int:service_id>', methods=['PUT'])
def edit_service(service_id):
    data = request.get_json(force=True)
    result, error = service.edit(service_id, data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 200


@service_bp.route('/servicos/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    ok, error = service.delete(service_id)
    if error:
        return jsonify({'erro': error}), 404
    return jsonify({'mensagem': 'Serviço excluído com sucesso'}), 200
