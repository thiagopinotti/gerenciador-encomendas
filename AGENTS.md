# AGENTS.md — API de Encomendas

## Visão Geral do Projeto

API REST para cadastro e gerenciamento de produtos e encomendas.
Desenvolvida com **FastAPI + SQLModel + Alembic**, gerenciada com **uv**.
Banco de dados: **SQLite local** (arquivo `database.db` na raiz do projeto).

---

## MCP Disponível: Context7

Este projeto usa o **Context7** como MCP de documentação. Ele fornece documentação atualizada das bibliotecas diretamente no contexto do agente, evitando alucinações de API e comportamentos de versões antigas.

### Regra obrigatória

**Antes de implementar qualquer código que use FastAPI, SQLModel, Alembic ou uv, consulte o Context7 para obter a documentação atualizada da biblioteca em questão.**

Exemplos de quando consultar:

- Antes de definir um model com `SQLModel` → buscar doc do SQLModel
- Antes de configurar o `alembic/env.py` → buscar doc do Alembic
- Antes de criar um router com `APIRouter` → buscar doc do FastAPI
- Em caso de dúvida sobre qualquer comportamento de lib → consultar antes de assumir

### Como usar no prompt

Inclua instruções como:

```
use context7 to fetch up-to-date documentation for SQLModel before implementing the models
use context7 to fetch up-to-date documentation for Alembic before configuring env.py
```

### Configuração no opencode (`~/.config/opencode/opencode.json`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "local",
      "command": ["npx", "-y", "@upstash/context7-mcp"],
      "enabled": true
    }
  }
}
```

---

## Stack e Versões

| Ferramenta   | Uso                            |
|--------------|--------------------------------|
| Python 3.12+ | Linguagem principal            |
| FastAPI       | Framework web / API            |
| SQLModel      | ORM + validação (Pydantic+SQLAlchemy) |
| Alembic       | Migrações do banco de dados    |
| uv            | Gerenciador de projeto e deps  |
| SQLite        | Banco de dados local           |

---

## Estrutura de Diretórios Esperada

```
.
├── AGENTS.md
├── pyproject.toml
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py              # Instância do FastAPI e inclusão dos routers
│   ├── database.py          # Engine SQLite e sessão
│   ├── models/
│   │   ├── __init__.py
│   │   ├── produto.py       # Tabela: produtos
│   │   ├── encomenda.py     # Tabela: encomendas
│   │   └── item_encomenda.py# Tabela: itens_encomenda
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── produto.py       # Schemas de entrada/saída para produtos
│   │   └── encomenda.py     # Schemas de entrada/saída para encomendas
│   └── routers/
│       ├── __init__.py
│       ├── produtos.py      # Endpoints de produtos
│       └── encomendas.py    # Endpoints de encomendas
└── database.db              # Gerado automaticamente (não versionar)
```

---

## Schema do Banco de Dados

```sql
-- Produtos
CREATE TABLE produtos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       VARCHAR NOT NULL,
    preco      DECIMAL NOT NULL,   -- Preço atual de venda
    estoque    INTEGER NOT NULL DEFAULT 0,
    criado_em  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Encomendas
CREATE TABLE encomendas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente      VARCHAR NOT NULL,
    data         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status       VARCHAR NOT NULL DEFAULT 'pendente',
    valor_sinal  DECIMAL NOT NULL DEFAULT 0  -- Quanto o cliente pagou adiantado
);

-- Itens de Encomenda
CREATE TABLE itens_encomenda (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    encomenda_id    INTEGER NOT NULL REFERENCES encomendas(id),
    produto_id      INTEGER NOT NULL REFERENCES produtos(id),
    quantidade      INTEGER NOT NULL,
    preco_unitario  DECIMAL NOT NULL  -- Snapshot do preço no momento do pedido
);
```

**Relações:**
- `itens_encomenda.encomenda_id` → `encomendas.id`
- `itens_encomenda.produto_id` → `produtos.id`

---

## Endpoints da API

### Produtos — `/produtos`

| Método | Rota              | Descrição                |
|--------|-------------------|--------------------------|
| POST   | `/produtos`       | Cadastrar produto        |
| GET    | `/produtos`       | Listar todos os produtos |
| PUT    | `/produtos/{id}`  | Editar produto           |
| DELETE | `/produtos/{id}`  | Remover produto          |

### Encomendas — `/encomendas`

| Método | Rota                  | Descrição                  |
|--------|-----------------------|----------------------------|
| POST   | `/encomendas`         | Cadastrar encomenda        |
| GET    | `/encomendas`         | Listar todas as encomendas |
| PUT    | `/encomendas/{id}`    | Editar encomenda           |
| DELETE | `/encomendas/{id}`    | Remover encomenda          |

---

## Regras de Negócio

1. **Snapshot de preço**: ao criar um item de encomenda, `preco_unitario` deve ser copiado do campo `preco` do produto no momento da criação — nunca calculado depois.
2. **Status de encomenda**: valores permitidos: `pendente`, `confirmada`, `em_producao`, `pronta`, `entregue`, `cancelada`.
3. **Remoção de produto**: não permitir se existirem `itens_encomenda` vinculados ao produto. Retornar HTTP 409 com mensagem clara.
4. **Remoção de encomenda**: remover em cascata os `itens_encomenda` vinculados.
5. **Estoque**: o campo `estoque` é informativo no momento atual — não há validação de disponibilidade na criação da encomenda.
6. **`criado_em` e `data`**: definidos automaticamente pelo banco; não devem ser aceitos no payload de criação.

---

## Padrões de Código

### Models (SQLModel)
- Usar `SQLModel` com `table=True` para as tabelas.
- Campos com valor padrão devem usar `Field(default=...)`.
- Separar `TableModel`, `CreateSchema` e `ReadSchema` em arquivos distintos ou como classes separadas no mesmo arquivo de model.

### Routers
- Um arquivo por recurso: `routers/produtos.py`, `routers/encomendas.py`.
- Usar `APIRouter` com `prefix` e `tags` definidos.
- Injetar sessão do banco via `Depends(get_session)`.

### Respostas HTTP
- `POST` → `201 Created` com o objeto criado.
- `GET` → `200 OK` com lista ou objeto.
- `PUT` → `200 OK` com objeto atualizado.
- `DELETE` → `204 No Content` (sem body).
- Recurso não encontrado → `404 Not Found`.
- Conflito de integridade → `409 Conflict`.

### Banco de Dados
- Engine criada em `app/database.py` com `create_engine("sqlite:///database.db")`.
- Sessão via `Session` do SQLModel com `yield` para uso com `Depends`.
- **Não** usar `SQLModel.metadata.create_all()` em produção — usar Alembic para todas as migrações.

---

## Configuração do Projeto com uv

```bash
# Criar projeto
uv init encomendas-api
cd encomendas-api

# Adicionar dependências
uv add fastapi sqlmodel alembic uvicorn

# Rodar a API
uv run uvicorn app.main:app --reload

# Criar migração
uv run alembic revision --autogenerate -m "descricao"

# Aplicar migrações
uv run alembic upgrade head
```

---

## Configuração do Alembic

Em `alembic/env.py`, garantir que o `target_metadata` aponte para os models do SQLModel:

```python
from app.models import *  # importar todos os models
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata
```

O `alembic.ini` deve ter:

```ini
sqlalchemy.url = sqlite:///database.db
```

---

## Arquivos a NÃO versionar (`.gitignore`)

```
database.db
__pycache__/
*.pyc
.venv/
.env
```

---

## Ordem de Implementação Sugerida

1. Criar estrutura de diretórios e `pyproject.toml` com uv.
2. Implementar `app/database.py` (engine + sessão).
3. Implementar models em `app/models/`.
4. Configurar Alembic e gerar a migração inicial.
5. Implementar schemas em `app/schemas/`.
6. Implementar routers em `app/routers/`.
7. Registrar routers em `app/main.py`.
8. Testar todos os endpoints via `/docs` (Swagger UI automático do FastAPI).

---

## Exemplo de Payload

### `POST /produtos`
```json
{
  "nome": "Bolo de chocolate",
  "preco": 45.00,
  "estoque": 10
}
```

### `POST /encomendas`
```json
{
  "cliente": "Maria Silva",
  "status": "pendente",
  "valor_sinal": 20.00,
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

> O campo `preco_unitario` de cada item é preenchido automaticamente com base no preço atual do produto — não deve ser enviado pelo cliente.
