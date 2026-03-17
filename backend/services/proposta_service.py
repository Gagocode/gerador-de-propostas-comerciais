import json
from backend.repositories.proposta_repository import PropostaRepository
from backend.repositories.cliente_repository import ClienteRepository
from backend.repositories.configuracao_repository import ConfiguracaoRepository


class PropostaService:

    def __init__(self):
        self.repo = PropostaRepository()
        self.cliente_repo = ClienteRepository()
        self.config_repo = ConfiguracaoRepository()

    def _build_snapshot(self, cliente_id, titulo, descricao, observacoes,
                        empresa_representante, empresa_cargo,
                        cliente_representante, cliente_cargo,
                        valor_total, status, servicos):
        cliente = None
        if cliente_id:
            c = self.cliente_repo.get_by_id(cliente_id)
            if c:
                cliente = c.to_dict()
        config = self.config_repo.get()
        return json.dumps({
            'titulo': titulo,
            'descricao': descricao,
            'observacoes': observacoes,
            'empresa_representante': empresa_representante,
            'empresa_cargo': empresa_cargo,
            'cliente_representante': cliente_representante,
            'cliente_cargo': cliente_cargo,
            'valor_total': valor_total,
            'status': status,
            'cliente': cliente,
            'servicos': servicos,
            'empresa': config.to_dict() if config else {},
        }, ensure_ascii=False)

    def _calc_total(self, servicos):
        return sum(float(s.get('valor', 0)) for s in servicos)

    def listar(self):
        return [p.to_dict() for p in self.repo.get_all()]

    def buscar(self, proposta_id):
        p = self.repo.get_by_id(proposta_id)
        if p is None:
            return None, 'Proposta não encontrada'
        return p.to_dict(), None

    def criar(self, dados):
        titulo = dados.get('titulo', '').strip()
        if not titulo:
            return None, 'Título é obrigatório'

        cliente_id = dados.get('cliente_id')
        descricao = dados.get('descricao', '')
        observacoes = dados.get('observacoes', '')
        empresa_representante = dados.get('empresa_representante', '')
        empresa_cargo = dados.get('empresa_cargo', '')
        cliente_representante = dados.get('cliente_representante', '')
        cliente_cargo = dados.get('cliente_cargo', '')
        servicos = dados.get('servicos', [])
        status = 'rascunho'
        valor_total = self._calc_total(servicos)
        snapshot = self._build_snapshot(
            cliente_id, titulo, descricao, observacoes,
            empresa_representante, empresa_cargo,
            cliente_representante, cliente_cargo,
            valor_total, status, servicos
        )

        p = self.repo.create(
            cliente_id, titulo, descricao, observacoes,
            empresa_representante, empresa_cargo,
            cliente_representante, cliente_cargo,
            valor_total, status, snapshot, servicos
        )
        return p.to_dict(), None

    def editar(self, proposta_id, dados):
        existente = self.repo.get_by_id(proposta_id)
        if existente is None:
            return None, 'Proposta não encontrada'
        if existente.status != 'rascunho':
            return None, 'Apenas propostas com status "rascunho" podem ser editadas'

        titulo = dados.get('titulo', '').strip()
        if not titulo:
            return None, 'Título é obrigatório'

        cliente_id = dados.get('cliente_id')
        descricao = dados.get('descricao', '')
        observacoes = dados.get('observacoes', '')
        empresa_representante = dados.get('empresa_representante', '')
        empresa_cargo = dados.get('empresa_cargo', '')
        cliente_representante = dados.get('cliente_representante', '')
        cliente_cargo = dados.get('cliente_cargo', '')
        servicos = dados.get('servicos', [])
        status = dados.get('status', existente.status)
        valor_total = self._calc_total(servicos)
        snapshot = self._build_snapshot(
            cliente_id, titulo, descricao, observacoes,
            empresa_representante, empresa_cargo,
            cliente_representante, cliente_cargo,
            valor_total, status, servicos
        )

        p = self.repo.update(
            proposta_id, cliente_id, titulo, descricao, observacoes,
            empresa_representante, empresa_cargo,
            cliente_representante, cliente_cargo,
            valor_total, status, snapshot, servicos
        )
        return p.to_dict(), None

    def duplicar(self, proposta_id):
        original = self.repo.get_by_id(proposta_id)
        if original is None:
            return None, 'Proposta não encontrada'

        servicos = [
            {
                'servico_id': s.servico_id,
                'nome': s.nome,
                'descricao': s.descricao,
                'valor': s.valor,
            }
            for s in original.servicos
        ]
        titulo = f'Cópia de {original.titulo}'
        status = 'rascunho'
        valor_total = original.valor_total
        snapshot = self._build_snapshot(
            original.cliente_id, titulo, original.descricao, original.observacoes,
            original.empresa_representante, original.empresa_cargo,
            original.cliente_representante, original.cliente_cargo,
            valor_total, status, servicos
        )

        nova = self.repo.create(
            original.cliente_id, titulo, original.descricao, original.observacoes,
            original.empresa_representante, original.empresa_cargo,
            original.cliente_representante, original.cliente_cargo,
            valor_total, status, snapshot, servicos
        )
        return nova.to_dict(), None
