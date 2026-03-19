from flask import Blueprint, request, jsonify
from backend.services.proposal_service import ProposalService

proposal_bp = Blueprint('proposals', __name__)
service = ProposalService()


@proposal_bp.route('/propostas', methods=['GET'])
def list_proposals():
    return jsonify(service.list_all()), 200


@proposal_bp.route('/propostas/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    result, error = service.get(proposal_id)
    if error:
        return jsonify({'erro': error}), 404
    return jsonify(result), 200


@proposal_bp.route('/propostas', methods=['POST'])
def create_proposal():
    data = request.get_json(force=True)
    result, error = service.create(data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 201


@proposal_bp.route('/propostas/<int:proposal_id>', methods=['PUT'])
def edit_proposal(proposal_id):
    data = request.get_json(force=True)
    result, error = service.edit(proposal_id, data)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 200


@proposal_bp.route('/propostas/<int:proposal_id>/duplicar', methods=['POST'])
def duplicate_proposal(proposal_id):
    result, error = service.duplicate(proposal_id)
    if error:
        return jsonify({'erro': error}), 400
    return jsonify(result), 201
