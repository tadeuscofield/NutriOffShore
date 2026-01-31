"""Rotas de Cardápios do Refeitório"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from datetime import date, timedelta

from app.database import get_db
from app.models.cardapio import Cardapio
from app.schemas.cardapio import CardapioCreate, CardapioResponse

router = APIRouter()


@router.post("/", response_model=CardapioResponse, status_code=201)
async def criar_cardapio(data: CardapioCreate, db: AsyncSession = Depends(get_db)):
    cardapio = Cardapio(
        plataforma_id=data.plataforma_id,
        data=data.data,
        refeicao=data.refeicao,
        itens=[item.model_dump() for item in data.itens],
    )
    db.add(cardapio)
    await db.commit()
    await db.refresh(cardapio)
    return cardapio


@router.get("/dia/{data_str}")
async def cardapio_do_dia(data_str: str, plataforma_id: UUID = None, db: AsyncSession = Depends(get_db)):
    data_cardapio = date.fromisoformat(data_str)
    stmt = select(Cardapio).where(Cardapio.data == data_cardapio)
    if plataforma_id:
        stmt = stmt.where(Cardapio.plataforma_id == plataforma_id)

    result = await db.execute(stmt)
    cardapios = result.scalars().all()

    refeicoes = {}
    for c in cardapios:
        refeicoes[c.refeicao] = {"id": str(c.id), "itens": c.itens}

    return {"data": data_str, "refeicoes": refeicoes}


@router.get("/semana")
async def cardapio_semana(plataforma_id: UUID = None, db: AsyncSession = Depends(get_db)):
    hoje = date.today()
    inicio = hoje - timedelta(days=hoje.weekday())
    fim = inicio + timedelta(days=6)

    stmt = select(Cardapio).where(
        and_(Cardapio.data >= inicio, Cardapio.data <= fim)
    ).order_by(Cardapio.data)

    if plataforma_id:
        stmt = stmt.where(Cardapio.plataforma_id == plataforma_id)

    result = await db.execute(stmt)
    cardapios = result.scalars().all()

    semana = {}
    for c in cardapios:
        dia = str(c.data)
        if dia not in semana:
            semana[dia] = {}
        semana[dia][c.refeicao] = c.itens

    return {"inicio": str(inicio), "fim": str(fim), "cardapios": semana}
