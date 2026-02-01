from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Any
from uuid import UUID

class PlanoCreate(BaseModel):
    colaborador_id: UUID
    meta_calorica: int = Field(..., gt=800, lt=6000)
    proteina_g: float = Field(..., gt=0, lt=1000)
    carboidratos_g: float = Field(..., gt=0, lt=2000)
    gorduras_g: float = Field(..., gt=0, lt=500)
    objetivo: Optional[str] = None
    refeicoes_detalhadas: Optional[list] = None
    suplementacao: Optional[Any] = None
    observacoes: Optional[str] = None
    data_inicio: date
    data_fim: Optional[date] = None

class PlanoUpdate(BaseModel):
    meta_calorica: Optional[int] = Field(None, gt=800, lt=6000)
    proteina_g: Optional[float] = Field(None, gt=0, lt=1000)
    carboidratos_g: Optional[float] = Field(None, gt=0, lt=2000)
    gorduras_g: Optional[float] = Field(None, gt=0, lt=500)
    objetivo: Optional[str] = None
    observacoes: Optional[str] = None
    data_fim: Optional[date] = None
    ativo: Optional[bool] = None

class PlanoResponse(BaseModel):
    id: UUID
    colaborador_id: UUID
    meta_calorica: int
    proteina_g: int
    carboidratos_g: int
    gorduras_g: int
    objetivo: Optional[str]
    refeicoes_detalhadas: Optional[list] = None
    suplementacao: Optional[Any]
    observacoes: Optional[str]
    data_inicio: date
    data_fim: Optional[date]
    ativo: bool
    created_by: str
    created_at: datetime
    class Config:
        from_attributes = True
