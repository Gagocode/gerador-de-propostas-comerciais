from backend.database.db import get_connection
from backend.models.proposal import Proposal, ProposalItem


class ProposalRepository:

    def _get_by_id(self, cursor, proposal_id):
        """Internal get_by_id using an existing cursor."""
        query = """
            SELECT p.*, 
                   c.name as client_name, c.email as client_email, c.phone as client_phone
            FROM proposals p
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE p.id = %s
        """
        cursor.execute(query, (proposal_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        
        p = Proposal.from_row(row)
        
        # Load services using the same cursor
        cursor.execute(
            "SELECT * FROM proposal_services WHERE proposal_id = %s", (p.id,)
        )
        p.services = [ProposalItem.from_row(r) for r in cursor.fetchall()]
        return p

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT p.*, 
                           c.name as client_name, c.email as client_email, c.phone as client_phone
                    FROM proposals p
                    LEFT JOIN clients c ON p.client_id = c.id
                    ORDER BY p.updated_at DESC
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Proposal.from_row(r) for r in rows]

    def get_by_id(self, proposal_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                return self._get_by_id(cursor, proposal_id)

    def create(self, client_id, title, description, notes,
               company_representative, company_role,
               client_representative, client_role,
               total_value, status, snapshot_json, services):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """INSERT INTO proposals
                       (client_id, title, description, notes,
                        company_representative, company_role,
                        client_representative, client_role,
                        total_value, status, snapshot_json)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (client_id, title, description, notes,
                     company_representative, company_role,
                     client_representative, client_role,
                     total_value, status, snapshot_json)
                )
                proposal_id = cursor.lastrowid
                for s in services:
                    cursor.execute(
                        """INSERT INTO proposal_services
                           (proposal_id, service_id, name, description, value)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (proposal_id, s.get('servico_id'), s['nome'],
                         s.get('descricao', ''), s['valor'])
                    )
                conn.commit()
                return self._get_by_id(cursor, proposal_id)

    def update(self, proposal_id, client_id, title, description, notes,
               company_representative, company_role,
               client_representative, client_role,
               total_value, status, snapshot_json, services):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """UPDATE proposals
                       SET client_id=%s, title=%s, description=%s, notes=%s,
                           company_representative=%s, company_role=%s,
                           client_representative=%s, client_role=%s,
                           total_value=%s, status=%s, snapshot_json=%s
                       WHERE id=%s""",
                    (client_id, title, description, notes,
                     company_representative, company_role,
                     client_representative, client_role,
                     total_value, status, snapshot_json, proposal_id)
                )
                cursor.execute(
                    "DELETE FROM proposal_services WHERE proposal_id=%s", (proposal_id,)
                )
                for s in services:
                    cursor.execute(
                        """INSERT INTO proposal_services
                           (proposal_id, service_id, name, description, value)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (proposal_id, s.get('servico_id'), s['nome'],
                         s.get('descricao', ''), s['valor'])
                    )
                conn.commit()
                return self._get_by_id(cursor, proposal_id)
