from backend.database.db import get_connection
from backend.models.proposal import Proposal, ProposalItem


class ProposalRepository:

    def _load_services(self, conn, proposal_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM proposal_services WHERE proposal_id = %s", (proposal_id,)
        )
        rows = cursor.fetchall()
        return [ProposalItem.from_row(r) for r in rows]

    def get_all(self):
        """Returns all proposals with client data joined (N+1 fix). Does NOT load services."""
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
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
        """Returns a single proposal with client data and services loaded."""
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
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
            p.services = self._load_services(conn, p.id)
            return p

    def create(self, client_id, title, description, notes,
               company_representative, company_role,
               client_representative, client_role,
               total_value, status, snapshot_json, services):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
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
            return self.get_by_id(proposal_id)

    def update(self, proposal_id, client_id, title, description, notes,
               company_representative, company_role,
               client_representative, client_role,
               total_value, status, snapshot_json, services):
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
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
            return self.get_by_id(proposal_id)
