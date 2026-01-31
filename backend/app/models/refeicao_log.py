import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class RefeicaoLog(Base):
    __tablename__ = "refeicoes_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    plano_id = Column(UUID(as_uuid=True), ForeignKey("planos_nutricionais.id"))
    data = Column(Date, nullable=False)
    refeicao = Column(String(20), nullable=False)
    itens_consumidos = Column(JSONB, nullable=False)
    calorias_estimadas = Column(Integer)
    proteina_g = Column(Integer)
    carboidratos_g = Column(Integer)
    gorduras_g = Column(Integer)
    aderencia_percentual = Column(Integer)
    observacoes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (CheckConstraint('aderencia_percentual BETWEEN 0 AND 100', name='check_aderencia'),)
    colaborador = relationship("Colaborador", back_populates="refeicoes")
    plano = relationship("PlanoNutricional", back_populates="refeicoes_log")
