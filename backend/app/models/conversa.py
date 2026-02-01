import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base

class ConversaAgente(Base):
    __tablename__ = "conversas_agente"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colaborador_id = Column(UUID(as_uuid=True), ForeignKey("colaboradores.id"), nullable=False, index=True)
    messages = Column(JSONB, nullable=False, default=list)
    tokens_utilizados = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    colaborador = relationship("Colaborador", back_populates="conversas")

    __table_args__ = (
        Index('ix_conversas_colab_updated', 'colaborador_id', 'updated_at'),
    )
