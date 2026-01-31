import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Text, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class CondicaoSaude(Base):
    __tablename__ = "condicoes_saude"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    condicao = Column(String(50), nullable=False)
    severidade = Column(String(20))
    data_diagnostico = Column(Date)
    medicamentos = Column(ARRAY(Text))
    observacoes = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="condicoes")
