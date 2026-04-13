# Projeto Encomendas

Monorepo para gestão de produtos e encomendas.

> **Status:** Backend em desenvolvimento ativo. Frontend em planejamento.

## Stack

- **Backend:** FastAPI + SQLModel + Alembic
- **Banco:** SQLite (produção futura: PostgreSQL)
- **Frontend:** Em desenvolvimento (stack a definir)
- **Gerenciador:** uv

## Estrutura

```
projeto-encomendas/
├── backend/          # API REST (FastAPI)
├── frontend/         # Frontend (a definir)
├── README.md         # Este arquivo
└── .gitignore
```

## Começando

### Backend

```bash
cd backend

# Instalar dependências
uv sync

# Aplicar migrações
uv run alembic upgrade head

# Rodar em desenvolvimento
uv run uvicorn app.main:app --reload --port 8000
```

### Frontend

Em desenvolvimento...

## Documentação da API

Após iniciar o servidor, akses:

- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI:** http://localhost:8000/openapi.json

## Roadmap

- [x] Backend API REST
- [ ] Frontend (stack a definir)
- [ ] Migração SQLite → PostgreSQL
- [ ] Autenticação
- [ ] Deploy

## Licença

Este projeto está em desenvolvimento.