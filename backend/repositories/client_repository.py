from backend.database.db import get_connection
from backend.models.client import Client


class ClientRepository:

    def get_all(self):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients ORDER BY name")
            rows = cursor.fetchall()
            return [Client.from_row(r) for r in rows]

    def get_by_id(self, client_id):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
            row = cursor.fetchone()
            return Client.from_row(row)

    def create(self, name, email, phone):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return self.get_by_id(new_id)

    def update(self, client_id, name, email, phone):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "UPDATE clients SET name=%s, email=%s, phone=%s WHERE id=%s",
                (name, email, phone, client_id)
            )
            conn.commit()
            return self.get_by_id(client_id)
