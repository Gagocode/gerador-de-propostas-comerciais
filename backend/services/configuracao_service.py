from backend.repositories.configuracao_repository import ConfiguracaoRepository


class ConfiguracaoService:

    def __init__(self):
        self.repo = ConfiguracaoRepository()

    def buscar(self):
        c = self.repo.get()
        return c.to_dict() if c else {}

    def salvar(self, dados):
        nome_empresa = dados.get('nome_empresa', '').strip()
        if not nome_empresa:
            return None, 'Nome da empresa é obrigatório'
        telefone = dados.get('telefone', '')
        email = dados.get('email', '')
        endereco = dados.get('endereco', '')
        rodape = dados.get('rodape', '')
        c = self.repo.update(nome_empresa, telefone, email, endereco, rodape)
        return c.to_dict(), None
