class PropostaServico:
    def __init__(self, id=None, proposta_id=None, servico_id=None,
                 nome='', descricao='', valor=0.0):
        self.id = id
        self.proposta_id = proposta_id
        self.servico_id = servico_id
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

    def to_dict(self):
        return {
            'id': self.id,
            'proposta_id': self.proposta_id,
            'servico_id': self.servico_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'valor': self.valor,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return PropostaServico(
            id=row['id'],
            proposta_id=row['proposta_id'],
            servico_id=row['servico_id'],
            nome=row['nome'],
            descricao=row['descricao'],
            valor=row['valor'],
        )


class Proposta:
    def __init__(self, id=None, cliente_id=None, titulo='', descricao='',
                 observacoes='', empresa_representante='', empresa_cargo='',
                 cliente_representante='', cliente_cargo='',
                 valor_total=0.0, status='rascunho', snapshot_json=None,
                 created_at=None, updated_at=None, cliente=None, servicos=None):
        self.id = id
        self.cliente_id = cliente_id
        self.titulo = titulo
        self.descricao = descricao
        self.observacoes = observacoes
        self.empresa_representante = empresa_representante
        self.empresa_cargo = empresa_cargo
        self.cliente_representante = cliente_representante
        self.cliente_cargo = cliente_cargo
        self.valor_total = valor_total
        self.status = status
        self.snapshot_json = snapshot_json
        self.created_at = created_at
        self.updated_at = updated_at
        self.cliente = cliente
        self.servicos = servicos or []

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'observacoes': self.observacoes,
            'empresa_representante': self.empresa_representante,
            'empresa_cargo': self.empresa_cargo,
            'cliente_representante': self.cliente_representante,
            'cliente_cargo': self.cliente_cargo,
            'valor_total': self.valor_total,
            'status': self.status,
            'snapshot_json': self.snapshot_json,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'servicos': [s.to_dict() for s in self.servicos],
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        
        # Helper para evitar erros caso a coluna não exista (embora a migração garanta)
        def get_val(r, key, default=''):
            try:
                return r[key] if r[key] is not None else default
            except:
                return default

        return Proposta(
            id=row['id'],
            cliente_id=row['cliente_id'],
            titulo=row['titulo'],
            descricao=get_val(row, 'descricao'),
            observacoes=get_val(row, 'observacoes'),
            empresa_representante=get_val(row, 'empresa_representante'),
            empresa_cargo=get_val(row, 'empresa_cargo'),
            cliente_representante=get_val(row, 'cliente_representante'),
            cliente_cargo=get_val(row, 'cliente_cargo'),
            valor_total=row['valor_total'],
            status=row['status'],
            snapshot_json=get_val(row, 'snapshot_json'),
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
