from flask import Blueprint, request, jsonify
from backend.services.proposta_service import PropostaService

proposta_bp = Blueprint('propostas', __name__)
service = PropostaService()


@proposta_bp.route('/propostas', methods=['GET'])
def listar():
    return jsonify(service.listar()), 200


@proposta_bp.route('/propostas/<int:proposta_id>', methods=['GET'])
def buscar(proposta_id):
    result, erro = service.buscar(proposta_id)
    if erro:
        return jsonify({'erro': erro}), 404
    return jsonify(result), 200


@proposta_bp.route('/propostas', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    result, erro = service.criar(dados)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 201


@proposta_bp.route('/propostas/<int:proposta_id>', methods=['PUT'])
def editar(proposta_id):
    dados = request.get_json(force=True)
    result, erro = service.editar(proposta_id, dados)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 200


@proposta_bp.route('/propostas/<int:proposta_id>/duplicar', methods=['POST'])
def duplicar(proposta_id):
    result, erro = service.duplicar(proposta_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(result), 201
