"""Rotas de Planos Nutricionais"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID

from app.database import get_db
from app.models.plano_nutricional import PlanoNutricional
from app.schemas.plano import PlanoCreate, PlanoUpdate, PlanoResponse

router = APIRouter()


@router.post("/", response_model=PlanoResponse, status_code=201)
async def criar_plano(data: PlanoCreate, db: AsyncSession = Depends(get_db)):
    # Desativar planos anteriores do colaborador
    stmt = select(PlanoNutricional).where(
        and_(PlanoNutricional.colaborador_id == data.colaborador_id, PlanoNutricional.ativo == True)
    )
    result = await db.execute(stmt)
    for plano in result.scalars().all():
        plano.ativo = False

    novo_plano = PlanoNutricional(**data.model_dump())
    db.add(novo_plano)
    await db.commit()
    await db.refresh(novo_plano)
    return novo_plano


@router.get("/colaborador/{colaborador_id}", response_model=list[PlanoResponse])
async def listar_planos_colaborador(colaborador_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(PlanoNutricional)
        .where(PlanoNutricional.colaborador_id == colaborador_id)
        .order_by(PlanoNutricional.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/colaborador/{colaborador_id}/ativo", response_model=PlanoResponse)
async def plano_ativo(colaborador_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(PlanoNutricional).where(
        and_(PlanoNutricional.colaborador_id == colaborador_id, PlanoNutricional.ativo == True)
    )
    result = await db.execute(stmt)
    plano = result.scalar_one_or_none()
    if not plano:
        raise HTTPException(status_code=404, detail="Nenhum plano ativo encontrado")
    return plano


@router.put("/{plano_id}", response_model=PlanoResponse)
async def atualizar_plano(plano_id: UUID, data: PlanoUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(PlanoNutricional).where(PlanoNutricional.id == plano_id)
    result = await db.execute(stmt)
    plano = result.scalar_one_or_none()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(plano, field, value)

    await db.commit()
    await db.refresh(plano)
    return plano


@router.delete("/{plano_id}", status_code=204)
async def deletar_plano(plano_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(PlanoNutricional).where(PlanoNutricional.id == plano_id)
    result = await db.execute(stmt)
    plano = result.scalar_one_or_none()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    await db.delete(plano)
    await db.commit()
