from backend.database.db import get_connection
from backend.models.servico import Servico


class ServicoRepository:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM servicos ORDER BY nome").fetchall()
        conn.close()
        return [Servico.from_row(r) for r in rows]

    def get_by_id(self, servico_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM servicos WHERE id = ?", (servico_id,)).fetchone()
        conn.close()
        return Servico.from_row(row)

    def create(self, nome, descricao, valor_padrao):
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO servicos (nome, descricao, valor_padrao) VALUES (?, ?, ?)",
            (nome, descricao, valor_padrao)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return self.get_by_id(new_id)

    def update(self, servico_id, nome, descricao, valor_padrao):
        conn = get_connection()
        conn.execute(
            "UPDATE servicos SET nome=?, descricao=?, valor_padrao=? WHERE id=?",
            (nome, descricao, valor_padrao, servico_id)
        )
        conn.commit()
        conn.close()
        return self.get_by_id(servico_id)

    def delete(self, servico_id):
        conn = get_connection()
        conn.execute("DELETE FROM servicos WHERE id=?", (servico_id,))
        conn.commit()
        conn.close()
