class Servico:
    def __init__(self, id=None, nome='', descricao='', valor_padrao=0.0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.valor_padrao = valor_padrao

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'valor_padrao': self.valor_padrao,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Servico(
            id=row['id'],
            nome=row['nome'],
            descricao=row['descricao'],
            valor_padrao=row['valor_padrao'],
        )
