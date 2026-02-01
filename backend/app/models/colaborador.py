import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, CHAR, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Colaborador(Base):
    __tablename__ = "colaboradores"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = Column(String(20), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(CHAR(1), nullable=False)
    altura_cm = Column(Numeric(5, 2))
    cargo = Column(String(100))
    nivel_atividade = Column(String(20), default="moderado")
    turno_atual = Column(String(10), default="diurno")
    regime_embarque = Column(String(10), default="14x14")
    meta_principal = Column(String(30), default="saude_geral")
    senha_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    medicoes = relationship("Medicao", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    condicoes = relationship("CondicaoSaude", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    preferencias = relationship("PreferenciaAlimentar", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    planos = relationship("PlanoNutricional", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    refeicoes = relationship("RefeicaoLog", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    alertas = relationship("AlertaMedico", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
    conversas = relationship("ConversaAgente", back_populates="colaborador", lazy="selectin", cascade="all, delete-orphan")
