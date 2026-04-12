from datetime import datetime
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    pendente = "pendente"
    confirmada = "confirmada"
    em_producao = "em_producao"
    pronta = "pronta"
    entregue = "entregue"
    cancelada = "cancelada"


class ItemEncomendaBase:
    produto_id: int
    quantidade: int


class ItemEncomendaCreate:
    produto_id: int
    quantidade: int


class ItemEncomendaRead:
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float


class EncomendaBase:
    cliente: str
    status: StatusEnum = StatusEnum.pendente
    valor_sinal: float = 0


class EncomendaCreate:
    cliente: str
    status: StatusEnum = StatusEnum.pendente
    valor_sinal: float = 0
    itens: list[ItemEncomendaCreate] = []


class EncomendaUpdate:
    cliente: Optional[str] = None
    status: Optional[StatusEnum] = None
    valor_sinal: Optional[float] = None


class EncomendaRead:
    id: int
    cliente: str
    data: datetime
    status: StatusEnum
    valor_sinal: float
    itens: list[ItemEncomendaRead] = []
