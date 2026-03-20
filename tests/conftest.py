import pytest
import os
import tempfile
import sqlite3
from backend.database.db import init_db
import backend.database.db as db_module
from backend.services.proposal_service import ProposalService
from backend.repositories.client_repository import ClientRepository

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """
    Configura um banco de dados SQLite temporário para cada teste.
    Garante isolamento e evita efeitos colaterais entre os testes.
    """
    # Cria arquivo temporário para o banco
    fd, db_path = tempfile.mkstemp()
    os.close(fd)
    
    # Redireciona o DATABASE_PATH do módulo db_module diretamente
    # para usar o banco temporário.
    monkeypatch.setattr(db_module, "DATABASE_PATH", db_path)
    
    # Inicializa o esquema do banco
    init_db()
    
    yield db_path
    
    # Remove o arquivo após o teste
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def proposal_service():
    return ProposalService()

@pytest.fixture
def client_repo():
    return ClientRepository()
