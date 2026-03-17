from backend.database.db import get_connection
from backend.models.cliente import Cliente


class ClienteRepository:

    def get_all(self):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM clientes ORDER BY nome").fetchall()
        conn.close()
        return [Cliente.from_row(r) for r in rows]

    def get_by_id(self, cliente_id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        conn.close()
        return Cliente.from_row(row)

    def create(self, nome, email, telefone):
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return self.get_by_id(new_id)

    def update(self, cliente_id, nome, email, telefone):
        conn = get_connection()
        conn.execute(
            "UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?",
            (nome, email, telefone, cliente_id)
        )
        conn.commit()
        conn.close()
        return self.get_by_id(cliente_id)
