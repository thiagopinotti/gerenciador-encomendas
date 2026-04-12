from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.produto import Produto
from app.models.item_encomenda import ItemEncomenda

router = APIRouter(prefix="/produtos", tags=["produtos"])

SessionDep = Annotated[Session, Depends(get_session)]


class ProdutoCreateSchema(BaseModel):
    nome: str
    preco: float
    estoque: int = 0


class ProdutoUpdateSchema(BaseModel):
    nome: str | None = None
    preco: float | None = None
    estoque: int | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    criado_em: datetime

    model_config = {"from_attributes": True}


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_produto(produto: ProdutoCreateSchema, session: SessionDep) -> Produto:
    db_produto = Produto(**produto.model_dump())
    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)
    return db_produto


@router.get("/", response_model=list[ProdutoResponse])
def list_produtos(session: SessionDep) -> list[Produto]:
    produtos = session.exec(select(Produto)).all()
    return produtos


@router.get("/{produto_id}", response_model=ProdutoResponse)
def get_produto(produto_id: int, session: SessionDep) -> Produto:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def update_produto(
    produto_id: int, produto: ProdutoUpdateSchema, session: SessionDep
) -> Produto:
    db_produto = session.get(Produto, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    produto_data = produto.model_dump(exclude_unset=True)
    for key, value in produto_data.items():
        setattr(db_produto, key, value)

    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)
    return db_produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(produto_id: int, session: SessionDep) -> None:
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    itens = session.exec(
        select(ItemEncomenda).where(ItemEncomenda.produto_id == produto_id)
    ).all()
    if itens:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover produto com encomendas vinculadas",
        )

    session.delete(produto)
    session.commit()
