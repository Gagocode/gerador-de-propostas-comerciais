from flask import Blueprint, request, jsonify
from backend.services.configuration_service import ConfigurationService

configuration_bp = Blueprint('configurations', __name__)
service = ConfigurationService()


@configuration_bp.route('/configuracoes', methods=['GET'])
def get_config():
    return jsonify(service.get()), 200


@configuration_bp.route('/configuracoes', methods=['PUT'])
def save_config():
    data = request.get_json(force=True)
    result, error = service.save(data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 200
