import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SQLite (old)
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'proposta.db')

# MySQL (new)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'proposta_db')
DB_PORT = int(os.environ.get('DB_PORT', 3306))

DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
