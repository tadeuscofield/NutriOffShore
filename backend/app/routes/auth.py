"""Rotas de Autenticacao"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.colaborador import Colaborador
from app.auth import create_access_token, hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter()


class LoginRequest(BaseModel):
    matricula: str = Field(..., max_length=20)
    senha: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    matricula: str = Field(..., max_length=20)
    senha: str = Field(..., min_length=6)
    nome: str = Field(..., max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Autentica colaborador por matricula e senha, retorna JWT."""
    stmt = select(Colaborador).where(Colaborador.matricula == data.matricula)
    result = await db.execute(stmt)
    colaborador = result.scalar_one_or_none()

    if not colaborador or not colaborador.senha_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matricula ou senha invalida",
        )

    if not verify_password(data.senha, colaborador.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matricula ou senha invalida",
        )

    token = create_access_token(
        data={"sub": str(colaborador.id), "matricula": colaborador.matricula}
    )
    logger.info(f"Login bem-sucedido: matricula={data.matricula}")
    return TokenResponse(access_token=token)


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Registra novo colaborador com senha e retorna JWT."""
    # Verificar se matricula ja existe
    stmt = select(Colaborador).where(Colaborador.matricula == data.matricula)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # Se ja existe mas nao tem senha, permitir definir senha
        if not existing.senha_hash:
            existing.senha_hash = hash_password(data.senha)
            await db.commit()
            token = create_access_token(
                data={"sub": str(existing.id), "matricula": existing.matricula}
            )
            logger.info(f"Senha definida para colaborador existente: matricula={data.matricula}")
            return TokenResponse(access_token=token)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Matricula ja cadastrada",
        )

    # Criar novo colaborador com dados minimos
    # Campos obrigatorios recebem valores padrao temporarios
    from datetime import date

    colaborador = Colaborador(
        matricula=data.matricula,
        nome=data.nome,
        senha_hash=hash_password(data.senha),
        data_nascimento=date(2000, 1, 1),  # Placeholder — atualizar no perfil
        sexo="M",  # Placeholder — atualizar no perfil
    )
    db.add(colaborador)
    await db.commit()
    await db.refresh(colaborador)

    token = create_access_token(
        data={"sub": str(colaborador.id), "matricula": colaborador.matricula}
    )
    logger.info(f"Novo colaborador registrado: matricula={data.matricula}")
    return TokenResponse(access_token=token)
