from flask import Blueprint, request, jsonify
from backend.repositories.cliente_repository import ClienteRepository

cliente_bp = Blueprint('clientes', __name__)
repo = ClienteRepository()


@cliente_bp.route('/clientes', methods=['GET'])
def listar():
    clientes = repo.get_all()
    return jsonify([c.to_dict() for c in clientes]), 200


@cliente_bp.route('/clientes', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    nome = dados.get('nome', '').strip()
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    c = repo.create(nome, dados.get('email', ''), dados.get('telefone', ''))
    return jsonify(c.to_dict()), 201


@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def editar(cliente_id):
    dados = request.get_json(force=True)
    nome = dados.get('nome', '').strip()
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    c = repo.update(cliente_id, nome, dados.get('email', ''), dados.get('telefone', ''))
    return jsonify(c.to_dict()), 200
