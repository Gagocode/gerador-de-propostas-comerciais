from backend.repositories.service_repository import ServiceRepository


class ServiceService:

    def __init__(self):
        self.repo = ServiceRepository()

    def list_all(self):
        return [s.to_dict() for s in self.repo.get_all()]

    def get(self, service_id):
        s = self.repo.get_by_id(service_id)
        if not s:
            return None, 'Serviço não encontrado'
        return s.to_dict(), None

    def create(self, data):
        name = data.get('nome', '').strip()
        if not name:
            return None, 'Nome do serviço é obrigatório'
        description = data.get('descricao', '')
        default_value = data.get('valor_padrao', 0.0)
        s = self.repo.create(name, description, default_value)
        return s.to_dict(), None

    def edit(self, service_id, data):
        name = data.get('nome', '').strip()
        if not name:
            return None, 'Nome do serviço é obrigatório'
        description = data.get('descricao', '')
        default_value = data.get('valor_padrao', 0.0)
        s = self.repo.update(service_id, name, description, default_value)
        return s.to_dict(), None

    def delete(self, service_id):
        self.repo.delete(service_id)
        return True, None
