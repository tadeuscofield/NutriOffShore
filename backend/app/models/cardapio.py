import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base

class Cardapio(Base):
    __tablename__ = "cardapios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plataforma_id = Column(UUID(as_uuid=True), nullable=False)
    data = Column(Date, nullable=False)
    refeicao = Column(String(20), nullable=False)
    itens = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('plataforma_id', 'data', 'refeicao', name='uq_cardapio'),)
