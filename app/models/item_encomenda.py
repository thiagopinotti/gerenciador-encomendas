from typing import TYPE_CHECKING, Any

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.encomenda import Encomenda
    from app.models.produto import Produto


class ItemEncomenda(SQLModel, table=True):
    __tablename__: Any = "itens_encomenda"

    id: int | None = Field(default=None, primary_key=True)
    encomenda_id: int = Field(foreign_key="encomendas.id", index=True)
    produto_id: int = Field(foreign_key="produtos.id", index=True)
    quantidade: int
    preco_unitario: float

    encomenda: "Encomenda" = Relationship(back_populates="itens")
    produto: "Produto" = Relationship()
