import pytest
import os
import tempfile
import sqlite3
import mysql.connector
from backend.services.proposal_service import ProposalService
from backend.repositories.client_repository import ClientRepository
from unittest.mock import MagicMock, patch

class SQLiteMySQLAdapter:
    def __init__(self, sqlite_conn):
        self.conn = sqlite_conn
        self.conn.row_factory = sqlite3.Row

    def cursor(self, dictionary=False, buffered=False):
        # We ignore dictionary=True because row_factory = sqlite3.Row already handles it
        return SQLiteMySQLCursorAdapter(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def is_connected(self):
        # Check if the sqlite connection is still open
        try:
            self.conn.execute("SELECT 1")
            return True
        except:
            return False

class SQLiteMySQLCursorAdapter:
    def __init__(self, sqlite_cursor):
        self.cursor = sqlite_cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute(self, query, params=None, multi=False):
        # Replace MySQL %s placeholder with SQLite ?
        translated_query = query.replace('%s', '?')
        
        if params:
            self.cursor.execute(translated_query, params)
        else:
            self.cursor.execute(translated_query)
        return self

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()

@pytest.fixture(autouse=True)
def mock_mysql(monkeypatch):
    """
    Globally mocks mysql.connector.connect to return our SQLite adapter.
    """
    fd, db_path = tempfile.mkstemp()
    os.close(fd)
    
    # Initialize the test DB with SQLite schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    schema = """
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
            status TEXT NOT NULL DEFAULT 'draft',
            snapshot_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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
    """
    cursor.executescript(schema)
    cursor.execute("INSERT INTO configurations (company_name) VALUES ('My Company')")
    conn.commit()
    conn.close()

    def mock_connect(*args, **kwargs):
        # Return a new adapter around a new connection to the same file
        return SQLiteMySQLAdapter(sqlite3.connect(db_path))

    monkeypatch.setattr(mysql.connector, "connect", mock_connect)
    
    # Also need to mock the db_module.init_db to do nothing or use our mock
    import backend.database.db as db_module
    monkeypatch.setattr(db_module, "init_db", lambda: None)

    yield db_path
    
    # Wait a bit or ensure all connections are closed? 
    # The context managers in repositories should close them.
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            # On Windows, sometimes it takes a while to release the file
            pass

@pytest.fixture
def proposal_service():
    return ProposalService()

@pytest.fixture
def client_repo():
    return ClientRepository()
