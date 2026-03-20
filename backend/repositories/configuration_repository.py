from backend.database.db import get_connection
from backend.models.configuration import Configuration


class ConfigurationRepository:

    def get(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM configurations LIMIT 1")
                row = cursor.fetchone()
                return Configuration.from_row(row)

    def update(self, company_name, phone, email, address, footer):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Check if exists
                cursor.execute("SELECT id FROM configurations LIMIT 1")
                row = cursor.fetchone()
                
                if row:
                    cursor.execute(
                        """UPDATE configurations 
                           SET company_name=%s, phone=%s, email=%s, address=%s, footer=%s
                           WHERE id=%s""",
                        (company_name, phone, email, address, footer, row['id'])
                    )
                else:
                    cursor.execute(
                        """INSERT INTO configurations 
                           (company_name, phone, email, address, footer)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (company_name, phone, email, address, footer)
                    )
                conn.commit()
                
                # Re-fetch using same connection
                cursor.execute("SELECT * FROM configurations LIMIT 1")
                return Configuration.from_row(cursor.fetchone())
