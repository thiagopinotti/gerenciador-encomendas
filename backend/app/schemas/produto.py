from datetime import datetime
from typing import Optional


class ProdutoBase:
    nome: str
    preco: float
    estoque: int = 0


class ProdutoCreate:
    nome: str
    preco: float
    estoque: int


class ProdutoUpdate:
    nome: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None


class ProdutoRead:
    id: int
    nome: str
    preco: float
    estoque: int
    criado_em: datetime
