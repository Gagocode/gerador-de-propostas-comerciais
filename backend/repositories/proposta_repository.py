from backend.database.db import get_connection
from backend.models.proposta import Proposta, PropostaServico
from backend.models.cliente import Cliente


class PropostaRepository:

    def _load_servicos(self, conn, proposta_id):
        rows = conn.execute(
            "SELECT * FROM proposta_servicos WHERE proposta_id = ?", (proposta_id,)
        ).fetchall()
        return [PropostaServico.from_row(r) for r in rows]

    def _load_cliente(self, conn, cliente_id):
        if cliente_id is None:
            return None
        row = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        return Cliente.from_row(row)

    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM propostas ORDER BY updated_at DESC"
        ).fetchall()
        result = []
        for row in rows:
            p = Proposta.from_row(row)
            p.cliente = self._load_cliente(conn, p.cliente_id)
            p.servicos = self._load_servicos(conn, p.id)
            result.append(p)
        conn.close()
        return result

    def get_by_id(self, proposta_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM propostas WHERE id = ?", (proposta_id,)
        ).fetchone()
        if row is None:
            conn.close()
            return None
        p = Proposta.from_row(row)
        p.cliente = self._load_cliente(conn, p.cliente_id)
        p.servicos = self._load_servicos(conn, p.id)
        conn.close()
        return p

    def create(self, cliente_id, titulo, descricao, observacoes,
               empresa_representante, empresa_cargo,
               cliente_representante, cliente_cargo,
               valor_total, status, snapshot_json, servicos):
        conn = get_connection()
        cursor = conn.execute(
            """INSERT INTO propostas
               (cliente_id, titulo, descricao, observacoes,
                empresa_representante, empresa_cargo,
                cliente_representante, cliente_cargo,
                valor_total, status, snapshot_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (cliente_id, titulo, descricao, observacoes,
             empresa_representante, empresa_cargo,
             cliente_representante, cliente_cargo,
             valor_total, status, snapshot_json)
        )
        proposta_id = cursor.lastrowid
        for s in servicos:
            conn.execute(
                """INSERT INTO proposta_servicos
                   (proposta_id, servico_id, nome, descricao, valor)
                   VALUES (?, ?, ?, ?, ?)""",
                (proposta_id, s.get('servico_id'), s['nome'],
                 s.get('descricao', ''), s['valor'])
            )
        conn.commit()
        conn.close()
        return self.get_by_id(proposta_id)

    def update(self, proposta_id, cliente_id, titulo, descricao, observacoes,
               empresa_representante, empresa_cargo,
               cliente_representante, cliente_cargo,
               valor_total, status, snapshot_json, servicos):
        conn = get_connection()
        conn.execute(
            """UPDATE propostas
               SET cliente_id=?, titulo=?, descricao=?, observacoes=?,
                   empresa_representante=?, empresa_cargo=?,
                   cliente_representante=?, cliente_cargo=?,
                   valor_total=?, status=?, snapshot_json=?,
                   updated_at=datetime('now','localtime')
               WHERE id=?""",
            (cliente_id, titulo, descricao, observacoes,
             empresa_representante, empresa_cargo,
             cliente_representante, cliente_cargo,
             valor_total, status, snapshot_json, proposta_id)
        )
        conn.execute(
            "DELETE FROM proposta_servicos WHERE proposta_id=?", (proposta_id,)
        )
        for s in servicos:
            conn.execute(
                """INSERT INTO proposta_servicos
                   (proposta_id, servico_id, nome, descricao, valor)
                   VALUES (?, ?, ?, ?, ?)""",
                (proposta_id, s.get('servico_id'), s['nome'],
                 s.get('descricao', ''), s['valor'])
            )
        conn.commit()
        conn.close()
        return self.get_by_id(proposta_id)
