from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

class ColaboradorBase(BaseModel):
    matricula: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=100)
    data_nascimento: date
    sexo: str = Field(..., pattern="^[MF]$")
    altura_cm: Optional[float] = None
    cargo: Optional[str] = None
    nivel_atividade: Optional[str] = "moderado"
    turno_atual: Optional[str] = "diurno"
    regime_embarque: Optional[str] = "14x14"
    meta_principal: Optional[str] = "saude_geral"

class ColaboradorCreate(ColaboradorBase):
    pass

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = None
    altura_cm: Optional[float] = None
    cargo: Optional[str] = None
    nivel_atividade: Optional[str] = None
    turno_atual: Optional[str] = None
    regime_embarque: Optional[str] = None
    meta_principal: Optional[str] = None

class MedicaoSchema(BaseModel):
    data_medicao: date
    peso_kg: Optional[float] = None
    circunferencia_abdominal_cm: Optional[float] = None
    percentual_gordura: Optional[float] = None
    pressao_sistolica: Optional[int] = None
    pressao_diastolica: Optional[int] = None
    glicemia_jejum: Optional[float] = None
    colesterol_total: Optional[float] = None
    hdl: Optional[float] = None
    ldl: Optional[float] = None
    triglicerides: Optional[float] = None
    fonte: Optional[str] = "auto_relato"

class CondicaoSaudeSchema(BaseModel):
    condicao: str
    severidade: Optional[str] = None
    data_diagnostico: Optional[date] = None
    medicamentos: Optional[List[str]] = None
    observacoes: Optional[str] = None

class PreferenciaSchema(BaseModel):
    tipo: str
    item: str
    severidade: Optional[str] = None

class ColaboradorResponse(ColaboradorBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ColaboradorFullResponse(ColaboradorResponse):
    medicoes: List[MedicaoSchema] = []
    condicoes: List[CondicaoSaudeSchema] = []
    preferencias: List[PreferenciaSchema] = []
    class Config:
        from_attributes = True
