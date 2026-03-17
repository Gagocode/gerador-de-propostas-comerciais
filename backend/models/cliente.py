class Cliente:
    def __init__(self, id=None, nome='', email='', telefone=''):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Cliente(
            id=row['id'],
            nome=row['nome'],
            email=row['email'],
            telefone=row['telefone'],
        )
