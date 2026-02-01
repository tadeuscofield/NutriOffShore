"""Rotas de Colaboradores"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import date

from app.database import get_db
from app.auth import get_current_user
from app.models.colaborador import Colaborador
from app.models.medicao import Medicao
from app.models.condicao_saude import CondicaoSaude
from app.models.preferencia_alimentar import PreferenciaAlimentar
from app.schemas.colaborador import (
    ColaboradorCreate, ColaboradorUpdate, ColaboradorResponse,
    ColaboradorFullResponse, MedicaoSchema, CondicaoSaudeSchema, PreferenciaSchema
)

router = APIRouter()


def _check_ownership(colaborador_id: UUID, current_user: dict) -> None:
    """Verifica se o colaborador_id pertence ao usuario autenticado."""
    if str(colaborador_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Acesso negado")


@router.post("/", response_model=ColaboradorResponse, status_code=201)
async def criar_colaborador(
    data: ColaboradorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    colaborador = Colaborador(**data.model_dump())
    db.add(colaborador)
    await db.commit()
    await db.refresh(colaborador)
    return colaborador


@router.get("/", response_model=list[ColaboradorResponse])
async def listar_colaboradores(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Escopo: retorna apenas o proprio colaborador
    user_id = current_user["sub"]
    stmt = (
        select(Colaborador)
        .where(Colaborador.id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Colaborador.nome)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{colaborador_id}", response_model=ColaboradorFullResponse)
async def buscar_colaborador(
    colaborador_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    stmt = (
        select(Colaborador)
        .options(
            selectinload(Colaborador.medicoes),
            selectinload(Colaborador.condicoes),
            selectinload(Colaborador.preferencias),
        )
        .where(Colaborador.id == colaborador_id)
    )
    result = await db.execute(stmt)
    colaborador = result.scalar_one_or_none()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador


@router.put("/{colaborador_id}", response_model=ColaboradorResponse)
async def atualizar_colaborador(
    colaborador_id: UUID,
    data: ColaboradorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    stmt = select(Colaborador).where(Colaborador.id == colaborador_id)
    result = await db.execute(stmt)
    colaborador = result.scalar_one_or_none()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(colaborador, field, value)

    await db.commit()
    await db.refresh(colaborador)
    return colaborador


@router.delete("/{colaborador_id}", status_code=204)
async def deletar_colaborador(
    colaborador_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    stmt = select(Colaborador).where(Colaborador.id == colaborador_id)
    result = await db.execute(stmt)
    colaborador = result.scalar_one_or_none()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    await db.delete(colaborador)
    await db.commit()


@router.post("/{colaborador_id}/medicoes", status_code=201)
async def registrar_medicao(
    colaborador_id: UUID,
    data: MedicaoSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    medicao = Medicao(colaborador_id=colaborador_id, **data.model_dump())
    db.add(medicao)
    await db.commit()
    await db.refresh(medicao)
    return {"id": str(medicao.id), "mensagem": "Medição registrada"}


@router.get("/{colaborador_id}/medicoes")
async def listar_medicoes(
    colaborador_id: UUID,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    stmt = (
        select(Medicao)
        .where(Medicao.colaborador_id == colaborador_id)
        .order_by(Medicao.data_medicao.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/{colaborador_id}/condicoes", status_code=201)
async def registrar_condicao(
    colaborador_id: UUID,
    data: CondicaoSaudeSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    condicao = CondicaoSaude(colaborador_id=colaborador_id, **data.model_dump())
    db.add(condicao)
    await db.commit()
    return {"mensagem": "Condição de saúde registrada"}


@router.post("/{colaborador_id}/preferencias", status_code=201)
async def registrar_preferencia(
    colaborador_id: UUID,
    data: PreferenciaSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_ownership(colaborador_id, current_user)
    pref = PreferenciaAlimentar(colaborador_id=colaborador_id, **data.model_dump())
    db.add(pref)
    await db.commit()
    return {"mensagem": "Preferência registrada"}
