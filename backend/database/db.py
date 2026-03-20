import mysql.connector
from mysql.connector import Error
import os
from contextlib import contextmanager
from backend.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


@contextmanager
def get_connection():
    """Context manager for MySQL database connections. Handles rollback and auto-close."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    try:
        yield conn
    except Exception as e:
        if conn.is_connected():
            conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if conn.is_connected():
            conn.close()


def init_db():
    """Initializes the MySQL database with tables and seed data."""
    # First connection to create the database if it doesn't exist
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()

    # Second connection to initialize tables
    with get_connection() as conn:
        cursor = conn.cursor()

        # Multi-statement execution for schema
        schema = """
            CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(50)
            );

            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                default_value DECIMAL(10, 2) NOT NULL DEFAULT 0.0
            );

            CREATE TABLE IF NOT EXISTS proposals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                notes TEXT,
                company_representative VARCHAR(255),
                company_role VARCHAR(255),
                client_representative VARCHAR(255),
                client_role VARCHAR(255),
                total_value DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
                status VARCHAR(20) NOT NULL DEFAULT 'draft',
                snapshot_json LONGTEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id),
                CONSTRAINT chk_status CHECK (status IN ('draft','sent','approved','rejected'))
            );

            CREATE TABLE IF NOT EXISTS proposal_services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                proposal_id INT NOT NULL,
                service_id INT,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                value DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
                FOREIGN KEY (proposal_id) REFERENCES proposals(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS configurations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL DEFAULT 'My Company',
                phone VARCHAR(50),
                email VARCHAR(255),
                address TEXT,
                footer TEXT
            );
        """
        
        # Execute schema queries individually
        for query in schema.split(';'):
            query = query.strip()
            if query:
                cursor.execute(query)

        # Seed default config if empty
        cursor.execute("SELECT COUNT(*) FROM configurations")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO configurations (company_name, phone, email, address, footer)
                VALUES (%s, %s, %s, %s, %s)
            """, ('My Company', '(00) 00000-0000', 'contact@company.com',
                  'Example Street, 123 - City, ST', 'Thank you for your business!'))

        conn.commit()
