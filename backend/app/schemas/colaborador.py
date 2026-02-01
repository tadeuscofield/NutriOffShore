from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, Literal
from uuid import UUID

class ColaboradorCreate(BaseModel):
    matricula: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=100)
    data_nascimento: date
    sexo: Literal["M", "F"]
    altura_cm: Optional[float] = Field(None, gt=50, lt=280)
    cargo: Optional[str] = None
    nivel_atividade: Literal["sedentario", "leve", "moderado", "intenso", "muito_intenso"] = "moderado"
    turno_atual: Literal["diurno", "noturno"] = "diurno"
    regime_embarque: Literal["14x14", "14x21", "21x21", "28x28"] = "14x14"
    meta_principal: Literal["perda_peso", "perda_gordura", "ganho_massa", "manutencao", "saude_geral", "performance"] = "saude_geral"

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = None
    altura_cm: Optional[float] = Field(None, gt=50, lt=280)
    cargo: Optional[str] = None
    nivel_atividade: Optional[Literal["sedentario", "leve", "moderado", "intenso", "muito_intenso"]] = None
    turno_atual: Optional[Literal["diurno", "noturno"]] = None
    regime_embarque: Optional[Literal["14x14", "14x21", "21x21", "28x28"]] = None
    meta_principal: Optional[Literal["perda_peso", "perda_gordura", "ganho_massa", "manutencao", "saude_geral", "performance"]] = None
    sexo: Optional[Literal["M", "F"]] = None

class MedicaoSchema(BaseModel):
    data_medicao: date
    peso_kg: float = Field(..., gt=20, lt=400)
    circunferencia_abdominal_cm: Optional[float] = Field(None, gt=30, lt=250)
    percentual_gordura: Optional[float] = Field(None, ge=1, le=70)
    pressao_sistolica: Optional[int] = Field(None, gt=50, lt=300)
    pressao_diastolica: Optional[int] = Field(None, gt=30, lt=200)
    glicemia_jejum: Optional[float] = Field(None, gt=20, lt=600)
    colesterol_total: Optional[float] = Field(None, gt=50, lt=500)
    hdl: Optional[float] = Field(None, gt=10, lt=200)
    ldl: Optional[float] = Field(None, gt=10, lt=400)
    triglicerides: Optional[float] = Field(None, gt=10, lt=1000)
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

class ColaboradorResponse(BaseModel):
    """Response schema - uses str for enum fields to tolerate existing DB data."""
    id: UUID
    matricula: str
    nome: str
    data_nascimento: date
    sexo: str
    altura_cm: Optional[float] = None
    cargo: Optional[str] = None
    nivel_atividade: str = "moderado"
    turno_atual: str = "diurno"
    regime_embarque: str = "14x14"
    meta_principal: str = "saude_geral"
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
