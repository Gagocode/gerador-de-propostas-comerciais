from backend.repositories.configuration_repository import ConfigurationRepository


class ConfigurationService:

    def __init__(self):
        self.repo = ConfigurationRepository()

    def get(self):
        c = self.repo.get()
        return c.to_dict() if c else {}

    def save(self, data):
        company_name = data.get('nome_empresa', '').strip()
        if not company_name:
            return None, 'Nome da empresa é obrigatório'
        phone = data.get('telefone', '')
        email = data.get('email', '')
        address = data.get('endereco', '')
        footer = data.get('rodape', '')
        c = self.repo.update(company_name, phone, email, address, footer)
        return c.to_dict(), None
