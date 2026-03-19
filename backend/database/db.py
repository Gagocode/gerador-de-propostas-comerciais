import sqlite3
import os
from contextlib import contextmanager
from backend.config import DATABASE_PATH


@contextmanager
def get_connection():
    """Context manager for database connections. Handles auto-close."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initializes the database with English table and column names."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT
            );

            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                default_value REAL NOT NULL DEFAULT 0.0
            );

            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                notes TEXT,
                company_representative TEXT,
                company_role TEXT,
                client_representative TEXT,
                client_role TEXT,
                total_value REAL NOT NULL DEFAULT 0.0,
                status TEXT NOT NULL DEFAULT 'draft'
                    CHECK(status IN ('draft','sent','approved','rejected')),
                snapshot_json TEXT,
                created_at DATETIME DEFAULT (datetime('now','localtime')),
                updated_at DATETIME DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (client_id) REFERENCES clients(id)
            );

            CREATE TABLE IF NOT EXISTS proposal_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_id INTEGER NOT NULL,
                service_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                value REAL NOT NULL DEFAULT 0.0,
                FOREIGN KEY (proposal_id) REFERENCES proposals(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL DEFAULT 'My Company',
                phone TEXT,
                email TEXT,
                address TEXT,
                footer TEXT
            );
        """)

        # Seed default config if empty
        cursor.execute("SELECT COUNT(*) FROM configurations")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO configurations (company_name, phone, email, address, footer)
                VALUES ('My Company', '(00) 00000-0000', 'contact@company.com',
                        'Example Street, 123 - City, ST', 'Thank you for your business!')
            """)

        conn.commit()
