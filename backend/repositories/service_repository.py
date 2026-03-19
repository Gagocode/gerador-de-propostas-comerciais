from backend.database.db import get_connection
from backend.models.service import Service


class ServiceRepository:

    def get_all(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM services ORDER BY name").fetchall()
            return [Service.from_row(r) for r in rows]

    def get_by_id(self, service_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
            return Service.from_row(row)

    def create(self, name, description, default_value):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO services (name, description, default_value) VALUES (?, ?, ?)",
                (name, description, default_value)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return self.get_by_id(new_id)

    def update(self, service_id, name, description, default_value):
        with get_connection() as conn:
            conn.execute(
                "UPDATE services SET name=?, description=?, default_value=? WHERE id=?",
                (name, description, default_value, service_id)
            )
            conn.commit()
            return self.get_by_id(service_id)

    def delete(self, service_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM services WHERE id=?", (service_id,))
            conn.commit()
