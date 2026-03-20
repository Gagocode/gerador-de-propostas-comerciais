from backend.database.db import get_connection
from backend.models.service import Service


class ServiceRepository:

    def _get_by_id(self, cursor, service_id):
        """Internal get_by_id using an existing cursor."""
        cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
        row = cursor.fetchone()
        return Service.from_row(row)

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM services ORDER BY name")
                rows = cursor.fetchall()
                return [Service.from_row(r) for r in rows]

    def get_by_id(self, service_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                return self._get_by_id(cursor, service_id)

    def create(self, name, description, default_value):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "INSERT INTO services (name, description, default_value) VALUES (%s, %s, %s)",
                    (name, description, default_value)
                )
                new_id = cursor.lastrowid
                conn.commit()
                return self._get_by_id(cursor, new_id)

    def update(self, service_id, name, description, default_value):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "UPDATE services SET name=%s, description=%s, default_value=%s WHERE id=%s",
                    (name, description, default_value, service_id)
                )
                conn.commit()
                return self._get_by_id(cursor, service_id)

    def delete(self, service_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM services WHERE id=%s", (service_id,))
                conn.commit()
