from backend.database.db import get_connection
from backend.models.configuration import Configuration


class ConfigurationRepository:

    def get(self):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM configurations LIMIT 1").fetchone()
            return Configuration.from_row(row)

    def update(self, company_name, phone, email, address, footer):
        with get_connection() as conn:
            row = conn.execute("SELECT id FROM configurations LIMIT 1").fetchone()
            if row:
                conn.execute(
                    """UPDATE configurations
                       SET company_name=?, phone=?, email=?, address=?, footer=?
                       WHERE id=?""",
                    (company_name, phone, email, address, footer, row['id'])
                )
            else:
                conn.execute(
                    """INSERT INTO configurations
                       (company_name, phone, email, address, footer)
                       VALUES (?, ?, ?, ?, ?)""",
                    (company_name, phone, email, address, footer)
                )
            conn.commit()
            return self.get()
