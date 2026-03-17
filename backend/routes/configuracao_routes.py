from flask import Blueprint, request, jsonify
from backend.services.configuracao_service import ConfiguracaoService

config_bp = Blueprint('configuracoes', __name__)
service = ConfiguracaoService()


@config_bp.route('/configuracoes', methods=['GET'])
def buscar():
    return jsonify(service.buscar()), 200


@config_bp.route('/configuracoes', methods=['PUT'])
def salvar():
    dados = request.get_json(force=True)
    result, erro = service.salvar(dados)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 200
