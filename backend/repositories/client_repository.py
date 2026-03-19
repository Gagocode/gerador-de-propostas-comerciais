from backend.database.db import get_connection
from backend.models.client import Client


class ClientRepository:

    def get_all(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
            return [Client.from_row(r) for r in rows]

    def get_by_id(self, client_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
            return Client.from_row(row)

    def create(self, name, email, phone):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return self.get_by_id(new_id)

    def update(self, client_id, name, email, phone):
        with get_connection() as conn:
            conn.execute(
                "UPDATE clients SET name=?, email=?, phone=? WHERE id=?",
                (name, email, phone, client_id)
            )
            conn.commit()
            return self.get_by_id(client_id)
