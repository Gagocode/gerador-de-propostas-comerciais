class Configuration:
    def __init__(self, id=None, company_name='', phone='',
                 email='', address='', footer=''):
        self.id = id
        self.company_name = company_name
        self.phone = phone
        self.email = email
        self.address = address
        self.footer = footer

    def to_dict(self):
        """Returns the model in Portuguese keys for API compatibility."""
        return {
            'id': self.id,
            'nome_empresa': self.company_name,
            'telefone': self.phone,
            'email': self.email,
            'endereco': self.address,
            'rodape': self.footer,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Configuration(
            id=row['id'],
            company_name=row['company_name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            footer=row['footer'],
        )
