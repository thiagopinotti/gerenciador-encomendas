from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from datetime import datetime

from app.database import get_session
from app.models.encomenda import Encomenda
from app.models.item_encomenda import ItemEncomenda
from app.models.produto import Produto

router = APIRouter(prefix="/encomendas", tags=["encomendas"])

SessionDep = Annotated[Session, Depends(get_session)]


class ItemEncomendaCreateSchema(BaseModel):
    produto_id: int
    quantidade: int


class ItemEncomendaReadSchema(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    model_config = {"from_attributes": True}


class EncomendaCreateSchema(BaseModel):
    cliente: str
    status: str = "pendente"
    valor_sinal: float = 0
    itens: list[ItemEncomendaCreateSchema] = []


class EncomendaUpdateSchema(BaseModel):
    cliente: str | None = None
    status: str | None = None
    valor_sinal: float | None = None


class EncomendaReadSchema(BaseModel):
    id: int
    cliente: str
    data: datetime
    status: str
    valor_sinal: float
    itens: list[ItemEncomendaReadSchema] = []

    model_config = {"from_attributes": True}


@router.post(
    "/", response_model=EncomendaReadSchema, status_code=status.HTTP_201_CREATED
)
def create_encomenda(
    encomenda: EncomendaCreateSchema, session: SessionDep
) -> Encomenda:
    db_encomenda = Encomenda(
        cliente=encomenda.cliente,
        status=encomenda.status,
        valor_sinal=encomenda.valor_sinal,
    )
    session.add(db_encomenda)
    session.flush()

    for item in encomenda.itens:
        produto = session.get(Produto, item.produto_id)
        if not produto:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {item.produto_id} não encontrado",
            )

        db_item = ItemEncomenda(
            encomenda_id=db_encomenda.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco,
        )
        session.add(db_item)

    session.commit()
    session.refresh(db_encomenda)
    return db_encomenda


@router.get("/", response_model=list[EncomendaReadSchema])
def list_encomendas(session: SessionDep) -> list[Encomenda]:
    encomendas = session.exec(select(Encomenda)).all()
    return encomendas


@router.get("/{encomenda_id}", response_model=EncomendaReadSchema)
def get_encomenda(encomenda_id: int, session: SessionDep) -> Encomenda:
    encomenda = session.get(Encomenda, encomenda_id)
    if not encomenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Encomenda não encontrada"
        )
    return encomenda


@router.put("/{encomenda_id}", response_model=EncomendaReadSchema)
def update_encomenda(
    encomenda_id: int, encomenda: EncomendaUpdateSchema, session: SessionDep
) -> Encomenda:
    db_encomenda = session.get(Encomenda, encomenda_id)
    if not db_encomenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Encomenda não encontrada"
        )

    encomenda_data = encomenda.model_dump(exclude_unset=True)
    for key, value in encomenda_data.items():
        if value is not None:
            setattr(db_encomenda, key, value)

    session.add(db_encomenda)
    session.commit()
    session.refresh(db_encomenda)
    return db_encomenda


@router.delete("/{encomenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_encomenda(encomenda_id: int, session: SessionDep) -> None:
    encomenda = session.get(Encomenda, encomenda_id)
    if not encomenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Encomenda não encontrada"
        )

    itens = session.exec(
        select(ItemEncomenda).where(ItemEncomenda.encomenda_id == encomenda_id)
    ).all()
    for item in itens:
        session.delete(item)

    session.delete(encomenda)
    session.commit()
