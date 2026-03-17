import sqlite3
import os
from backend.config import DATABASE_PATH


def get_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            valor_padrao REAL NOT NULL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS propostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT,
            observacoes TEXT,
            empresa_representante TEXT,
            empresa_cargo TEXT,
            cliente_representante TEXT,
            cliente_cargo TEXT,
            valor_total REAL NOT NULL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'rascunho'
                CHECK(status IN ('rascunho','enviada','aprovada','recusada')),
            snapshot_json TEXT,
            created_at DATETIME DEFAULT (datetime('now','localtime')),
            updated_at DATETIME DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS proposta_servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposta_id INTEGER NOT NULL,
            servico_id INTEGER,
            nome TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (proposta_id) REFERENCES propostas(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_empresa TEXT NOT NULL DEFAULT 'Minha Empresa',
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            rodape TEXT
        );
    """)

    # Seed default config if empty
    cursor.execute("SELECT COUNT(*) FROM configuracoes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO configuracoes (nome_empresa, telefone, email, endereco, rodape)
            VALUES ('Minha Empresa', '(00) 00000-0000', 'contato@empresa.com',
                    'Rua Exemplo, 123 - Cidade, UF', 'Obrigado pela preferência!')
        """)

    conn.commit()
    conn.close()
