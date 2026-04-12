# API de Encomendas

API REST para cadastro e gerenciamento de produtos e encomendas.

> **Status:** Backend em desenvolvimento ativo. Frontend em planejamento.

## Stack

- **Backend:** FastAPI + SQLModel + Alembic
- **Banco:** SQLite (produção futura: PostgreSQL)
- **Gerenciador:** uv

## Funcionalidades

- Cadastro de produtos
- Gestão de encomendas com itens
- Snapshot de preços no momento da encomenda

## Começando

### Pré-requisitos

- Python 3.12+

### Instalação

```bash
# Instalar dependências
uv sync

# Aplicar migrações do banco de dados
uv run alembic upgrade head
```

### Rodar em desenvolvimento

```bash
uv run uvicorn app.main:app --reload --port 8000
```

## Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI:** http://localhost:8000/openapi.json

## Estrutura do Projeto

```
app/
├── database.py    # Configuração do banco
├── main.py        # Aplicação FastAPI
├── models/        # Modelos SQLModel
├── routers/       # Endpoints da API
└── schemas/       # Schemas Pydantic
alembic/
└── versions/      # Migrações do banco de dados
```

## Endpoints

### Produtos

| Método | Rota              | Descrição                |
|--------|-------------------|--------------------------|
| POST   | `/produtos/`      | Cadastrar produto        |
| GET    | `/produtos/`      | Listar todos os produtos |
| GET    | `/produtos/{id}`  | Buscar produto por ID    |
| PUT    | `/produtos/{id}`  | Atualizar produto        |
| DELETE | `/produtos/{id}`  | Remover produto          |

### Encomendas

| Método | Rota                  | Descrição                  |
|--------|-----------------------|----------------------------|
| POST   | `/encomendas/`        | Cadastrar encomenda        |
| GET    | `/encomendas/`        | Listar todas as encomendas |
| GET    | `/encomendas/{id}`    | Buscar encomenda por ID    |
| PUT    | `/encomendas/{id}`    | Atualizar encomenda        |
| DELETE | `/encomendas/{id}`    | Remover encomenda          |

## Roadmap

- [ ] Frontend (stack a definir)
- [ ] Migração SQLite → PostgreSQL
- [ ] Autenticação
- [ ] Deploy

## Licença

Este projeto está em desenvolvimento.
