"""Rotas de Alertas Médicos"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.auth import get_current_user
from app.models.alerta_medico import AlertaMedico

router = APIRouter()


@router.get("/")
async def listar_alertas(
    status: str = "aberto",
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    stmt = (
        select(AlertaMedico)
        .where(AlertaMedico.status == status)
        .order_by(AlertaMedico.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    alertas = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "colaborador_id": str(a.colaborador_id),
            "tipo": a.tipo,
            "motivo": a.motivo,
            "recomendacao": a.recomendacao,
            "status": a.status,
            "created_at": a.created_at.isoformat(),
        }
        for a in alertas
    ]


@router.get("/colaborador/{colaborador_id}")
async def alertas_colaborador(
    colaborador_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    stmt = (
        select(AlertaMedico)
        .where(AlertaMedico.colaborador_id == colaborador_id)
        .order_by(AlertaMedico.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.put("/{alerta_id}/visualizar")
async def marcar_visualizado(
    alerta_id: UUID,
    visualizado_por: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    stmt = select(AlertaMedico).where(AlertaMedico.id == alerta_id)
    result = await db.execute(stmt)
    alerta = result.scalar_one_or_none()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")

    alerta.status = "visualizado"
    alerta.visualizado_por = visualizado_por
    alerta.visualizado_em = datetime.utcnow()
    await db.commit()
    return {"mensagem": "Alerta marcado como visualizado"}


@router.put("/{alerta_id}/resolver")
async def resolver_alerta(
    alerta_id: UUID,
    visualizado_por: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    stmt = select(AlertaMedico).where(AlertaMedico.id == alerta_id)
    result = await db.execute(stmt)
    alerta = result.scalar_one_or_none()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")

    alerta.status = "resolvido"
    alerta.visualizado_por = visualizado_por
    alerta.visualizado_em = datetime.utcnow()
    await db.commit()
    return {"mensagem": "Alerta resolvido"}
