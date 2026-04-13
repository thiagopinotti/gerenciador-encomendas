from datetime import datetime, timezone
from typing import Any

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Produto(SQLModel, table=True):
    __tablename__: Any = "produtos"

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    preco: float
    estoque: int = Field(default=0)
    criado_em: datetime = Field(default_factory=utc_now)
