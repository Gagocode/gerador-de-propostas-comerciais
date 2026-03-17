# PropostaPRO - Sistema de Gestão de Propostas Comerciais

## 1. Visão Geral do Projeto

O **PropostaPRO** é uma aplicação web para criação, gestão e visualização de propostas comerciais. O sistema visa automatizar o fluxo de vendas, permitindo que o usuário cadastre clientes e serviços para gerar documentos profissionais de forma rápida.

### Principais Funcionalidades
*   **Gestão de Clientes**: Cadastro e edição de dados de contato.
*   **Catálogo de Serviços**: Registro de serviços com descrição e valores padrão.
*   **Criação de Propostas**: Formulário dinâmico para seleção de cliente, adição de múltiplos serviços e definição de descrição personalizada.
*   **Visualização Profissional**: Geração de um documento comercial estilizado (A4) pronto para impressão ou salvamento em PDF.
*   **Ciclo de Vida**: Controle de status da proposta (Rascunho, Enviada, Aprovada, Recusada).
*   **Configurações da Empresa**: Customização de dados do cabeçalho e rodapé do documento.
*   **Duplicação**: Funcionalidade para clonar propostas existentes.

## 2. Stack Tecnológica

*   **Backend**: Python 3.x com Flask.
*   **Banco de Dados**: SQLite3 (armazenado em `backend/database/proposta.db`).
*   **Frontend**: HTML5, CSS3 (Vanilla) e JavaScript (Vanilla ES6+).
*   **Comunicação**: API REST JSON.
*   **Dependências Principais**: `Flask`, `Flask-CORS`.

## 3. Estrutura do Projeto

O projeto segue uma arquitetura em camadas no backend e uma estrutura de arquivos estáticos organizada no frontend.

```text
proposta_system/
├── backend/
│   ├── app.py              # Ponto de entrada e configuração de rotas Flask
│   ├── config.py           # Variáveis de ambiente e constantes
│   ├── database/           # Conexão e inicialização do SQLite
│   ├── models/             # Classes de representação das entidades
│   ├── repositories/       # Camada de persistência (SQL)
│   ├── services/           # Regras de negócio
│   └── routes/             # Definição de endpoints (Blueprints)
├── frontend/
│   ├── pages/              # Telas HTML (clientes, serviços, propostas, etc.)
│   ├── components/         # Fragmentos reutilizáveis (ex: nav.html)
│   ├── css/                # Estilização global e de visualização
│   └── js/                 # Lógica de interface e chamadas à API
└── requirements.txt        # Dependências Python
```

### Responsabilidades
*   **Models**: Definem a estrutura dos objetos e conversão de/para dicionários.
*   **Repositories**: Única camada que executa comandos SQL e interage com o `sqlite3`.
*   **Services**: Intermediam a lógica entre rotas e repositórios (ex: cálculo de totais, duplicação).
*   **Routes**: Tratam requisições HTTP, validam parâmetros básicos e retornam JSON.
*   **Frontend JS**: `api.js` centraliza chamadas `fetch`; `utils.js` contém formatadores e UI helpers.

## 4. Modelos de Dados

### Cliente (`clientes`)
*   `id`: INTEGER (PK)
*   `nome`: TEXT (Not Null)
*   `email`: TEXT
*   `telefone`: TEXT

### Serviço (`servicos`)
*   `id`: INTEGER (PK)
*   `nome`: TEXT (Not Null)
*   `descricao`: TEXT
*   `valor_padrao`: REAL

### Proposta (`propostas`)
*   `id`: INTEGER (PK)
*   `cliente_id`: INTEGER (FK)
*   `titulo`: TEXT
*   `descricao`: TEXT
*   `valor_total`: REAL
*   `status`: TEXT ('rascunho', 'enviada', 'aprovada', 'recusada')
*   `snapshot_json`: TEXT (Armazena histórico/estado da proposta)
*   `created_at`: DATETIME
*   `updated_at`: DATETIME

### Itens da Proposta (`proposta_servicos`)
*   `id`: INTEGER (PK)
*   `proposta_id`: INTEGER (FK)
*   `servico_id`: INTEGER (FK - Opcional para permitir customização local)
*   `nome`: TEXT
*   `descricao`: TEXT
*   `valor`: REAL

### Configuração (`configuracoes`)
*   `id`: INTEGER (PK)
*   `nome_empresa`: TEXT
*   `telefone`: TEXT
*   `email`: TEXT
*   `endereco`: TEXT
*   `rodape`: TEXT

## 5. Fluxo da Aplicação

1.  **Requisição**: O frontend faz um `fetch` para um endpoint `/api/...`.
2.  **Roteamento**: `backend/app.py` direciona para o Blueprint em `backend/routes/`.
3.  **Processamento**: A rota chama o Service correspondente, que pode invocar um ou mais Repositories.
4.  **Persistência**: O Repository usa `get_connection()` para executar SQL no SQLite.
5.  **Resposta**: O Model converte o resultado em dicionário (`to_dict`), e a rota retorna como JSON (status 200 ou erro).

## 6. Funcionalidades Implementadas

*   [x] CRUD completo de Clientes.
*   [x] CRUD completo de Serviços.
*   [x] Listagem, criação e edição de Propostas.
*   [x] Cálculo automático do `valor_total` ao salvar proposta.
*   [x] Duplicação de propostas com prefixo "(Cópia)".
*   [x] Visualização de proposta em modo "Documento Comercial" (estilo A4).
*   [x] Configuração de dados da empresa para o cabeçalho/rodapé.
*   [x] Estilização para impressão (remocão de menus/botões).

## 7. Pontos Incompletos / Técnicos

*   **Validações**: A validação de dados no backend é básica (presença de campos obrigatórios).
*   **Snapshot**: O campo `snapshot_json` existe no banco mas não parece estar sendo plenamente utilizado para versionamento histórico no código atual.
*   **Imagens/Logos**: Existe o campo de logo nas configurações, mas o upload de arquivos não está implementado (usa-se texto/CSS por enquanto).
*   **Autenticação**: Não existe sistema de login ou controle de usuários (acesso público total).
*   **Dashboard**: A tela inicial é a listagem de propostas; não há um dashboard com métricas (gráficos, conversão).

## 8. Padrões e Convenções

*   **Backend**: Snake_case para funções e variáveis; PascalCase para classes.
*   **Frontend**: CamelCase para funções JS; Kebab-case para classes CSS.
*   **API**: Retornos sempre em JSON, com chaves de erro (`erro`) em caso de falha.
*   **Estilo**: Utilização de variáveis CSS (`:root`) para cores e bordas, facilitando manutenção.

## 9. Diretrizes para IA (IMPORTANTE)

Para futuras manutenções e evoluções:

*   **Fidelidade ao Padrão**: Siga o padrão de Repositório/Service já estabelecido.
*   **Não Inventar Dependências**: Não adicione bibliotecas externas (como SQLAlchemy ou React) sem solicitação explícita. Mantenha a stack minimalista (Flask + Vanilla JS).
*   **Surgicidade**: Ao alterar o frontend, prefira atualizar partes específicas do DOM em vez de recarregar a página inteira, mantendo a sensação de fluidez.
*   **Responsividade**: Toda nova tela deve ser responsiva e, no caso de visualizações de documentos, focar na fidelidade de impressão (A4).
*   **Segurança**: Não implemente hardcodes de credenciais ou caminhos absolutos de sistema. Use `backend/config.py`.
*   **Clareza**: Sempre explique o porquê de uma mudança técnica, especialmente se envolver alterações no schema do banco de dados.
