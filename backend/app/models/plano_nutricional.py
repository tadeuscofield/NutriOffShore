import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class PlanoNutricional(Base):
    __tablename__ = "planos_nutricionais"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    meta_calorica = Column(Integer, nullable=False)
    proteina_g = Column(Integer, nullable=False)
    carboidratos_g = Column(Integer, nullable=False)
    gorduras_g = Column(Integer, nullable=False)
    objetivo = Column(String(30))
    refeicoes_detalhadas = Column(JSONB)
    suplementacao = Column(JSONB)
    observacoes = Column(Text)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    ativo = Column(Boolean, default=True)
    created_by = Column(String(50), default="nutrioffshore_ai")
    created_at = Column(DateTime, default=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="planos")
    refeicoes_log = relationship("RefeicaoLog", back_populates="plano", lazy="selectin")
