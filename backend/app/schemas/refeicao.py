from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, Any
from uuid import UUID

class ItemConsumido(BaseModel):
    alimento: str
    quantidade: str
    calorias_estimadas: Optional[float] = None

class RefeicaoLogCreate(BaseModel):
    colaborador_id: UUID
    plano_id: Optional[UUID] = None
    data: date
    refeicao: str
    itens_consumidos: List[ItemConsumido]
    calorias_estimadas: Optional[int] = None
    proteina_g: Optional[int] = None
    carboidratos_g: Optional[int] = None
    gorduras_g: Optional[int] = None
    aderencia_percentual: Optional[int] = Field(None, ge=0, le=100)
    observacoes: Optional[str] = None

class RefeicaoLogResponse(BaseModel):
    id: UUID
    colaborador_id: UUID
    plano_id: Optional[UUID]
    data: date
    refeicao: str
    itens_consumidos: Any
    calorias_estimadas: Optional[int]
    aderencia_percentual: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

class ResumoDiario(BaseModel):
    data: date
    total_calorias: int = 0
    total_proteina_g: int = 0
    total_carboidratos_g: int = 0
    total_gorduras_g: int = 0
    refeicoes_registradas: int = 0
    aderencia_media: Optional[int] = None
