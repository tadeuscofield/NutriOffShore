import uuid
from datetime import datetime
from sqlalchemy import Column, Date, Numeric, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Medicao(Base):
    __tablename__ = "medicoes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    data_medicao = Column(Date, nullable=False)
    peso_kg = Column(Numeric(5, 2))
    circunferencia_abdominal_cm = Column(Numeric(5, 2))
    percentual_gordura = Column(Numeric(4, 2))
    pressao_sistolica = Column(Integer)
    pressao_diastolica = Column(Integer)
    glicemia_jejum = Column(Numeric(5, 1))
    colesterol_total = Column(Numeric(5, 1))
    hdl = Column(Numeric(5, 1))
    ldl = Column(Numeric(5, 1))
    triglicerides = Column(Numeric(5, 1))
    fonte = Column(String(20), default="auto_relato")
    created_at = Column(DateTime, default=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="medicoes")
