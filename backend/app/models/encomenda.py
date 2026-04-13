from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.item_encomenda import ItemEncomenda


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Encomenda(SQLModel, table=True):
    __tablename__: Any = "encomendas"

    id: int | None = Field(default=None, primary_key=True)
    cliente: str = Field(index=True)
    data: datetime = Field(default_factory=utc_now)
    status: str = Field(default="pendente", index=True)
    valor_sinal: float = Field(default=0)

    itens: list["ItemEncomenda"] = Relationship(back_populates="encomenda")
