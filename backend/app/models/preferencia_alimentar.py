import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class PreferenciaAlimentar(Base):
    __tablename__ = "preferencias_alimentares"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False)
    tipo = Column(String(30), nullable=False)
    item = Column(String(100), nullable=False)
    severidade = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="preferencias")
