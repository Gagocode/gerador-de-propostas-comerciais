# PropostaPRO — Sistema de Propostas Comerciais

MVP completo para criação e gestão de propostas comerciais, desenvolvido com Flask + SQLite + HTML/CSS/JS puro.

---

## 🚀 Como rodar o projeto

### Pré-requisitos
- Python 3.9 ou superior
- pip

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o servidor

```bash
python -m backend.app
```

O sistema estará disponível em: **http://localhost:5000**

---

## 📁 Estrutura do projeto

```
proposta_system/
├── backend/
│   ├── app.py                  # Entrypoint Flask + rotas de arquivos estáticos
│   ├── config.py               # Configurações (porta, debug, path do banco)
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py               # Conexão SQLite + criação de schema + seed
│   ├── models/
│   │   ├── cliente.py
│   │   ├── servico.py
│   │   ├── proposta.py
│   │   └── configuracao.py
│   ├── repositories/
│   │   ├── cliente_repository.py
│   │   ├── servico_repository.py
│   │   ├── proposta_repository.py
│   │   └── configuracao_repository.py
│   ├── services/
│   │   ├── proposta_service.py   # Regras de negócio (snapshot, bloqueio, duplicação)
│   │   ├── servico_service.py
│   │   └── configuracao_service.py
│   └── routes/
│       ├── proposta_routes.py
│       ├── servico_routes.py
│       ├── configuracao_routes.py
│       └── cliente_routes.py
├── frontend/
│   ├── css/
│   │   └── style.css             # Design system + estilos de impressão (@media print A4)
│   ├── js/
│   │   ├── api.js                # Cliente HTTP centralizado
│   │   └── utils.js              # Funções utilitárias compartilhadas
│   ├── components/
│   │   └── nav.html              # Navegação compartilhada (carregada via fetch)
│   └── pages/
│       ├── propostas.html        # Lista de propostas
│       ├── proposta-form.html    # Criar / Editar proposta
│       ├── proposta-view.html    # Visualizar + Imprimir proposta
│       ├── servicos.html         # CRUD de serviços
│       ├── clientes.html         # CRUD de clientes
│       └── configuracoes.html    # Configurações da empresa
├── requirements.txt
└── README.md
```

---

## ⚙️ Regras de negócio implementadas

| Regra | Implementação |
|-------|--------------|
| **Snapshot** | Toda criação/edição salva JSON completo com cliente, serviços e valores em `snapshot_json` |
| **Bloqueio de edição** | Propostas com status diferente de "rascunho" não podem ser editadas (API + UI) |
| **Duplicação** | `POST /api/propostas/:id/duplicar` — cria nova proposta rascunho com todos os serviços copiados |
| **Valores fixos** | `proposta_servicos` armazena cópia dos dados — mudanças no catálogo não afetam propostas existentes |

---

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/propostas` | Listar todas as propostas |
| GET | `/api/propostas/:id` | Buscar proposta por ID |
| POST | `/api/propostas` | Criar proposta |
| PUT | `/api/propostas/:id` | Editar proposta (apenas rascunho) |
| POST | `/api/propostas/:id/duplicar` | Duplicar proposta |
| GET | `/api/servicos` | Listar serviços |
| POST | `/api/servicos` | Criar serviço |
| PUT | `/api/servicos/:id` | Editar serviço |
| DELETE | `/api/servicos/:id` | Excluir serviço |
| GET | `/api/clientes` | Listar clientes |
| POST | `/api/clientes` | Criar cliente |
| PUT | `/api/clientes/:id` | Editar cliente |
| GET | `/api/configuracoes` | Buscar configurações da empresa |
| PUT | `/api/configuracoes` | Salvar configurações |

---

## 🖨️ Impressão

Na página de visualização de proposta, clique em **"🖨️ Imprimir"**.  
O CSS aplica layout A4 profissional com `@media print`:
- Cabeçalho com dados da empresa
- Tabela de serviços
- Total em destaque
- Rodapé configurável
- Elementos de UI ocultados automaticamente

---

## 🗄️ Banco de dados

O arquivo `backend/database/proposta.db` é criado automaticamente na primeira execução. Não é necessário nenhum script SQL manual.
