class Configuracao:
    def __init__(self, id=None, nome_empresa='', telefone='',
                 email='', endereco='', rodape=''):
        self.id = id
        self.nome_empresa = nome_empresa
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.rodape = rodape

    def to_dict(self):
        return {
            'id': self.id,
            'nome_empresa': self.nome_empresa,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'rodape': self.rodape,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Configuracao(
            id=row['id'],
            nome_empresa=row['nome_empresa'],
            telefone=row['telefone'],
            email=row['email'],
            endereco=row['endereco'],
            rodape=row['rodape'],
        )
