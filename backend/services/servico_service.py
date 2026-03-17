from backend.repositories.servico_repository import ServicoRepository


class ServicoService:

    def __init__(self):
        self.repo = ServicoRepository()

    def listar(self):
        return [s.to_dict() for s in self.repo.get_all()]

    def criar(self, dados):
        nome = dados.get('nome', '').strip()
        if not nome:
            return None, 'Nome é obrigatório'
        descricao = dados.get('descricao', '')
        valor_padrao = float(dados.get('valor_padrao', 0))
        s = self.repo.create(nome, descricao, valor_padrao)
        return s.to_dict(), None

    def editar(self, servico_id, dados):
        existente = self.repo.get_by_id(servico_id)
        if existente is None:
            return None, 'Serviço não encontrado'
        nome = dados.get('nome', '').strip()
        if not nome:
            return None, 'Nome é obrigatório'
        descricao = dados.get('descricao', '')
        valor_padrao = float(dados.get('valor_padrao', 0))
        s = self.repo.update(servico_id, nome, descricao, valor_padrao)
        return s.to_dict(), None

    def excluir(self, servico_id):
        existente = self.repo.get_by_id(servico_id)
        if existente is None:
            return False, 'Serviço não encontrado'
        self.repo.delete(servico_id)
        return True, None
