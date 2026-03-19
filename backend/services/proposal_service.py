import json
from backend.repositories.proposal_repository import ProposalRepository
from backend.repositories.client_repository import ClientRepository
from backend.repositories.configuration_repository import ConfigurationRepository
from backend.models.proposal import STATUS_MAP_PT_TO_EN, STATUS_MAP_EN_TO_PT


class ProposalService:

    def __init__(self):
        self.repo = ProposalRepository()
        self.client_repo = ClientRepository()
        self.config_repo = ConfigurationRepository()

    def _build_snapshot(self, client_id, title, description, notes,
                        company_representative, company_role,
                        client_representative, client_role,
                        total_value, status, services):
        client = None
        if client_id:
            c = self.client_repo.get_by_id(client_id)
            if c:
                client = c.to_dict()
        config = self.config_repo.get()
        
        # Ensure status in snapshot is Portuguese for the View page
        status_pt = STATUS_MAP_EN_TO_PT.get(status, status)
        
        return json.dumps({
            'titulo': title,
            'descricao': description,
            'observacoes': notes,
            'empresa_representante': company_representative,
            'empresa_cargo': company_role,
            'cliente_representante': client_representative,
            'cliente_cargo': client_role,
            'valor_total': total_value,
            'status': status_pt,
            'cliente': client,
            'servicos': services,
            'empresa': config.to_dict() if config else {},
        }, ensure_ascii=False)

    def _calc_total(self, services):
        return sum(float(s.get('valor', 0)) for s in services)

    def list_all(self):
        return [p.to_dict() for p in self.repo.get_all()]

    def get(self, proposal_id):
        p = self.repo.get_by_id(proposal_id)
        if p is None:
            return None, 'Proposta não encontrada'
        return p.to_dict(), None

    def create(self, data):
        title = data.get('titulo', '').strip()
        if not title:
            return None, 'Título é obrigatório'

        client_id = data.get('cliente_id')
        description = data.get('descricao', '')
        notes = data.get('observacoes', '')
        company_representative = data.get('empresa_representante', '')
        company_role = data.get('empresa_cargo', '')
        client_representative = data.get('cliente_representante', '')
        client_role = data.get('cliente_cargo', '')
        services = data.get('servicos', [])
        status = 'draft'
        total_value = self._calc_total(services)
        snapshot = self._build_snapshot(
            client_id, title, description, notes,
            company_representative, company_role,
            client_representative, client_role,
            total_value, status, services
        )

        p = self.repo.create(
            client_id, title, description, notes,
            company_representative, company_role,
            client_representative, client_role,
            total_value, status, snapshot, services
        )
        return p.to_dict(), None

    def edit(self, proposal_id, data):
        existing = self.repo.get_by_id(proposal_id)
        if existing is None:
            return None, 'Proposta não encontrada'
        if existing.status != 'draft':
            return None, 'Apenas propostas com status "rascunho" podem ser editadas'

        title = data.get('titulo', '').strip()
        if not title:
            return None, 'Título é obrigatório'

        client_id = data.get('cliente_id')
        description = data.get('descricao', '')
        notes = data.get('observacoes', '')
        company_representative = data.get('empresa_representante', '')
        company_role = data.get('empresa_cargo', '')
        client_representative = data.get('cliente_representante', '')
        client_role = data.get('cliente_cargo', '')
        services = data.get('servicos', [])
        
        status_pt = data.get('status', '')
        status = STATUS_MAP_PT_TO_EN.get(status_pt, existing.status)
        
        total_value = self._calc_total(services)
        snapshot = self._build_snapshot(
            client_id, title, description, notes,
            company_representative, company_role,
            client_representative, client_role,
            total_value, status, services
        )

        p = self.repo.update(
            proposal_id, client_id, title, description, notes,
            company_representative, company_role,
            client_representative, client_role,
            total_value, status, snapshot, services
        )
        return p.to_dict(), None

    def duplicate(self, proposal_id):
        original = self.repo.get_by_id(proposal_id)
        if original is None:
            return None, 'Proposta não encontrada'

        services = [
            {
                'servico_id': s.service_id,
                'nome': s.name,
                'descricao': s.description,
                'valor': s.value,
            }
            for s in original.services
        ]
        title = f'Cópia de {original.title}'
        status = 'draft'
        total_value = original.total_value
        snapshot = self._build_snapshot(
            original.client_id, title, original.description, original.notes,
            original.company_representative, original.company_role,
            original.client_representative, original.client_role,
            total_value, status, services
        )

        new_proposal = self.repo.create(
            original.client_id, title, original.description, original.notes,
            original.company_representative, original.company_role,
            original.client_representative, original.client_role,
            total_value, status, snapshot, services
        )
        return new_proposal.to_dict(), None
