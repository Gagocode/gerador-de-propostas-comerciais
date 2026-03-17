from backend.database.db import get_connection
from backend.models.configuracao import Configuracao


class ConfiguracaoRepository:

    def get(self):
        conn = get_connection()
        row = conn.execute("SELECT * FROM configuracoes LIMIT 1").fetchone()
        conn.close()
        return Configuracao.from_row(row)

    def update(self, nome_empresa, telefone, email, endereco, rodape):
        conn = get_connection()
        row = conn.execute("SELECT id FROM configuracoes LIMIT 1").fetchone()
        if row:
            conn.execute(
                """UPDATE configuracoes
                   SET nome_empresa=?, telefone=?, email=?, endereco=?, rodape=?
                   WHERE id=?""",
                (nome_empresa, telefone, email, endereco, rodape, row['id'])
            )
        else:
            conn.execute(
                """INSERT INTO configuracoes
                   (nome_empresa, telefone, email, endereco, rodape)
                   VALUES (?, ?, ?, ?, ?)""",
                (nome_empresa, telefone, email, endereco, rodape)
            )
        conn.commit()
        conn.close()
        return self.get()
