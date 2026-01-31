import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class AlertaMedico(Base):
    __tablename__ = "alertas_medicos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    motivo = Column(Text, nullable=False)
    recomendacao = Column(Text)
    status = Column(String(20), default="aberto")
    visualizado_por = Column(String(100))
    visualizado_em = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="alertas")
