from backend.models.client import Client

# Status mapping for English (Internal) <-> Portuguese (External)
STATUS_MAP_EN_TO_PT = {
    'draft': 'rascunho',
    'sent': 'enviada',
    'approved': 'aprovada',
    'rejected': 'recusada'
}

STATUS_MAP_PT_TO_EN = {v: k for k, v in STATUS_MAP_EN_TO_PT.items()}

class ProposalItem:
    def __init__(self, id=None, proposal_id=None, service_id=None,
                 name='', description='', value=0.0):
        self.id = id
        self.proposal_id = proposal_id
        self.service_id = service_id
        self.name = name
        self.description = description
        self.value = value

    def to_dict(self):
        """Returns the model in Portuguese keys for API compatibility."""
        return {
            'id': self.id,
            'proposta_id': self.proposal_id,
            'servico_id': self.service_id,
            'nome': self.name,
            'descricao': self.description,
            'valor': self.value,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return ProposalItem(
            id=row['id'],
            proposal_id=row['proposal_id'],
            service_id=row['service_id'],
            name=row['name'],
            description=row['description'],
            value=float(row['value']) if row['value'] is not None else 0.0,
        )


class Proposal:
    def __init__(self, id=None, client_id=None, title='', description='',
                 notes='', company_representative='', company_role='',
                 client_representative='', client_role='',
                 total_value=0.0, status='draft', snapshot_json=None,
                 created_at=None, updated_at=None, client=None, services=None):
        self.id = id
        self.client_id = client_id
        self.title = title
        self.description = description
        self.notes = notes
        self.company_representative = company_representative
        self.company_role = company_role
        self.client_representative = client_representative
        self.client_role = client_role
        self.total_value = total_value
        self.status = status
        self.snapshot_json = snapshot_json
        self.created_at = created_at
        self.updated_at = updated_at
        self.client = client
        self.services = services or []

    def to_dict(self):
        """Returns the model in Portuguese keys for API compatibility."""
        # Map internal English status to Portuguese
        pt_status = STATUS_MAP_EN_TO_PT.get(self.status, self.status)
        
        return {
            'id': self.id,
            'cliente_id': self.client_id,
            'cliente': self.client.to_dict() if self.client else None,
            'titulo': self.title,
            'descricao': self.description,
            'observacoes': self.notes,
            'empresa_representante': self.company_representative,
            'empresa_cargo': self.company_role,
            'cliente_representante': self.client_representative,
            'cliente_cargo': self.client_role,
            'valor_total': self.total_value,
            'status': pt_status,
            'snapshot_json': self.snapshot_json,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at,
            'updated_at': self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else self.updated_at,
            'servicos': [s.to_dict() for s in self.services],
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        
        def get_val(r, key, default=''):
            try:
                return r[key] if r[key] is not None else default
            except:
                return default

        proposal = Proposal(
            id=row['id'],
            client_id=row['client_id'],
            title=row['title'],
            description=get_val(row, 'description'),
            notes=get_val(row, 'notes'),
            company_representative=get_val(row, 'company_representative'),
            company_role=get_val(row, 'company_role'),
            client_representative=get_val(row, 'client_representative'),
            client_role=get_val(row, 'client_role'),
            total_value=float(row['total_value']) if row['total_value'] is not None else 0.0,
            status=row['status'],
            snapshot_json=get_val(row, 'snapshot_json'),
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )

        if 'client_name' in row.keys():
            proposal.client = Client(
                id=row['client_id'],
                name=row['client_name'],
                email=get_val(row, 'client_email'),
                phone=get_val(row, 'client_phone')
            )
        
        return proposal
