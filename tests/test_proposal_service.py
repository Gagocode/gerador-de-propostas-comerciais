import json
import pytest

def test_create_proposal_valid(proposal_service, client_repo):
    """
    Testa se uma proposta válida é criada corretamente no banco de dados,
    com o ID do cliente correto e os serviços persistidos.
    """
    # Setup: Cria um cliente para a proposta
    client = client_repo.create("Cliente Teste", "teste@exemplo.com", "11999999999")
    
    data = {
        'titulo': 'Proposta de Teste',
        'cliente_id': client.id,
        'descricao': 'Descrição da proposta',
        'servicos': [
            {'nome': 'Serviço 1', 'valor': 100.0, 'descricao': 'Desc 1'},
            {'nome': 'Serviço 2', 'valor': 250.5, 'descricao': 'Desc 2'}
        ]
    }
    
    # Act: Cria a proposta
    proposal, error = proposal_service.create(data)
    
    # Assert
    assert error is None
    assert proposal['titulo'] == 'Proposta de Teste'
    assert proposal['cliente_id'] == client.id
    assert len(proposal['servicos']) == 2
    assert proposal['valor_total'] == 350.5
    assert proposal['status'] == 'rascunho'

def test_calculate_total_value(proposal_service):
    """
    Valida se o cálculo do total da proposta está sendo realizado corretamente
    pelo serviço.
    """
    # Act: Chama o método privado de cálculo diretamente para teste unitário
    total = proposal_service._calc_total([
        {'valor': 10},
        {'valor': '20.5'},
        {'valor': 0}
    ])
    
    # Assert
    assert total == 30.5

def test_persistence_and_retrieval(proposal_service, client_repo):
    """
    Garante que uma proposta criada pode ser recuperada pelo ID com consistência de dados.
    """
    # Setup
    client = client_repo.create("Cliente B", "b@exemplo.com", "")
    data = {
        'titulo': 'Persistência',
        'cliente_id': client.id,
        'servicos': [{'nome': 'S1', 'valor': 50}]
    }
    
    created, _ = proposal_service.create(data)
    
    # Act: Recupera a proposta do banco
    retrieved, error = proposal_service.get(created['id'])
    
    # Assert
    assert error is None
    assert retrieved['id'] == created['id']
    assert retrieved['titulo'] == 'Persistência'
    assert retrieved['valor_total'] == 50
    assert len(retrieved['servicos']) == 1
    assert retrieved['servicos'][0]['nome'] == 'S1'

def test_snapshot_generation(proposal_service, client_repo):
    """
    Valida se o snapshot_json da proposta está sendo gerado e mantém 
    os dados esperados para consulta histórica.
    """
    # Setup
    client = client_repo.create("Cliente Snapshot", "snap@exemplo.com", "123456")
    data = {
        'titulo': 'Teste Snapshot',
        'cliente_id': client.id,
        'servicos': [{'nome': 'S1', 'valor': 100, 'descricao': 'Desc S1'}]
    }
    
    # Act
    proposal, _ = proposal_service.create(data)
    snapshot = json.loads(proposal['snapshot_json'])
    
    # Assert: Verifica se o snapshot contém os dados congelados do cliente e serviços
    assert snapshot['titulo'] == 'Teste Snapshot'
    assert snapshot['cliente']['nome'] == "Cliente Snapshot"
    assert snapshot['cliente']['email'] == "snap@exemplo.com"
    assert len(snapshot['servicos']) == 1
    assert snapshot['servicos'][0]['nome'] == 'S1'
    assert snapshot['valor_total'] == 100
    assert 'empresa' in snapshot # Verifica se dados da empresa foram incluídos
