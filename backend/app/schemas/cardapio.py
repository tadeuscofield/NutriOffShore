from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Any, List
from uuid import UUID

class ItemCardapio(BaseModel):
    item: str
    categoria: str
    calorias_porcao: Optional[float] = None
    proteina_g: Optional[float] = None
    carb_g: Optional[float] = None
    gordura_g: Optional[float] = None
    indice_glicemico: Optional[str] = None

class CardapioCreate(BaseModel):
    plataforma_id: UUID
    data: date
    refeicao: str
    itens: List[ItemCardapio]

class CardapioResponse(BaseModel):
    id: UUID
    plataforma_id: UUID
    data: date
    refeicao: str
    itens: Any
    created_at: datetime
    class Config:
        from_attributes = True
