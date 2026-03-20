from backend.database.db import get_connection
from backend.models.client import Client


class ClientRepository:

    def _get_by_id(self, cursor, client_id):
        """Internal get_by_id using an existing cursor."""
        cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        row = cursor.fetchone()
        return Client.from_row(row)

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM clients ORDER BY name")
                rows = cursor.fetchall()
                return [Client.from_row(r) for r in rows]

    def get_by_id(self, client_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                return self._get_by_id(cursor, client_id)

    def create(self, name, email, phone):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)",
                    (name, email, phone)
                )
                new_id = cursor.lastrowid
                conn.commit()
                return self._get_by_id(cursor, new_id)

    def update(self, client_id, name, email, phone):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "UPDATE clients SET name=%s, email=%s, phone=%s WHERE id=%s",
                    (name, email, phone, client_id)
                )
                conn.commit()
                return self._get_by_id(cursor, client_id)
