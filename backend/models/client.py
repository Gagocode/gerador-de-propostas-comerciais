class Client:
    def __init__(self, id=None, name='', email='', phone=''):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Returns the model in Portuguese keys for API compatibility."""
        return {
            'id': self.id,
            'nome': self.name,
            'email': self.email,
            'telefone': self.phone,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Client(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
        )
