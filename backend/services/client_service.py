from backend.repositories.client_repository import ClientRepository


class ClientService:

    def __init__(self):
        self.repo = ClientRepository()

    def list_all(self):
        clients = self.repo.get_all()
        return [c.to_dict() for c in clients]

    def get(self, client_id):
        client = self.repo.get_by_id(client_id)
        if not client:
            return None, 'Cliente não encontrado'
        return client.to_dict(), None

    def create(self, data):
        name = data.get('nome', '').strip()
        if not name:
            return None, 'Nome é obrigatório'
        email = data.get('email', '')
        phone = data.get('telefone', '')
        client = self.repo.create(name, email, phone)
        return client.to_dict(), None

    def update(self, client_id, data):
        name = data.get('nome', '').strip()
        if not name:
            return None, 'Nome é obrigatório'
        email = data.get('email', '')
        phone = data.get('telefone', '')
        client = self.repo.update(client_id, name, email, phone)
        if not client:
            return None, 'Erro ao atualizar cliente'
        return client.to_dict(), None
