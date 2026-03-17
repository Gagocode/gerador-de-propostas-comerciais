from flask import Blueprint, request, jsonify
from backend.services.servico_service import ServicoService

servico_bp = Blueprint('servicos', __name__)
service = ServicoService()


@servico_bp.route('/servicos', methods=['GET'])
def listar():
    return jsonify(service.listar()), 200


@servico_bp.route('/servicos', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    result, erro = service.criar(dados)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 201


@servico_bp.route('/servicos/<int:servico_id>', methods=['PUT'])
def editar(servico_id):
    dados = request.get_json(force=True)
    result, erro = service.editar(servico_id, dados)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 200


@servico_bp.route('/servicos/<int:servico_id>', methods=['DELETE'])
def excluir(servico_id):
    ok, erro = service.excluir(servico_id)
    if erro:
        return jsonify({'erro': erro}), 404
    return jsonify({'mensagem': 'Serviço excluído com sucesso'}), 200
