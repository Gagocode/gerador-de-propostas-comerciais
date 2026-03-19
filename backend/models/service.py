class Service:
    def __init__(self, id=None, name='', description='', default_value=0.0):
        self.id = id
        self.name = name
        self.description = description
        self.default_value = default_value

    def to_dict(self):
        """Returns the model in Portuguese keys for API compatibility."""
        return {
            'id': self.id,
            'nome': self.name,
            'descricao': self.description,
            'valor_padrao': self.default_value,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Service(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            default_value=row['default_value'],
        )
