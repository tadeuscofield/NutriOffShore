"""Rotas de Registro de Refeições"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from uuid import UUID
from datetime import date, timedelta

from app.database import get_db
from app.models.refeicao_log import RefeicaoLog
from app.schemas.refeicao import RefeicaoLogCreate, RefeicaoLogResponse, ResumoDiario

router = APIRouter()


@router.post("/", response_model=RefeicaoLogResponse, status_code=201)
async def registrar_refeicao(data: RefeicaoLogCreate, db: AsyncSession = Depends(get_db)):
    log = RefeicaoLog(
        colaborador_id=data.colaborador_id,
        plano_id=data.plano_id,
        data=data.data,
        refeicao=data.refeicao,
        itens_consumidos=[item.model_dump() for item in data.itens_consumidos],
        calorias_estimadas=data.calorias_estimadas or sum(
            i.calorias_estimadas or 0 for i in data.itens_consumidos
        ),
        proteina_g=data.proteina_g,
        carboidratos_g=data.carboidratos_g,
        gorduras_g=data.gorduras_g,
        aderencia_percentual=data.aderencia_percentual,
        observacoes=data.observacoes,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/colaborador/{colaborador_id}/dia/{data_str}")
async def refeicoes_do_dia(
    colaborador_id: UUID, data_str: str, db: AsyncSession = Depends(get_db)
):
    data_ref = date.fromisoformat(data_str)
    stmt = (
        select(RefeicaoLog)
        .where(and_(RefeicaoLog.colaborador_id == colaborador_id, RefeicaoLog.data == data_ref))
        .order_by(RefeicaoLog.created_at)
    )
    result = await db.execute(stmt)
    refeicoes = result.scalars().all()

    total_cal = sum(r.calorias_estimadas or 0 for r in refeicoes)
    total_prot = sum(r.proteina_g or 0 for r in refeicoes)
    total_carb = sum(r.carboidratos_g or 0 for r in refeicoes)
    total_gord = sum(r.gorduras_g or 0 for r in refeicoes)

    return {
        "data": data_str,
        "refeicoes": [
            {
                "id": str(r.id),
                "refeicao": r.refeicao,
                "itens": r.itens_consumidos,
                "calorias": r.calorias_estimadas,
                "aderencia": r.aderencia_percentual,
            }
            for r in refeicoes
        ],
        "totais": {
            "calorias": total_cal,
            "proteina_g": total_prot,
            "carboidratos_g": total_carb,
            "gorduras_g": total_gord,
        },
    }


@router.get("/colaborador/{colaborador_id}/resumo-semanal")
async def resumo_semanal(colaborador_id: UUID, db: AsyncSession = Depends(get_db)):
    hoje = date.today()
    inicio = hoje - timedelta(days=6)

    stmt = (
        select(RefeicaoLog)
        .where(
            and_(
                RefeicaoLog.colaborador_id == colaborador_id,
                RefeicaoLog.data >= inicio,
            )
        )
        .order_by(RefeicaoLog.data)
    )
    result = await db.execute(stmt)
    refeicoes = result.scalars().all()

    dias = {}
    for r in refeicoes:
        dia = str(r.data)
        if dia not in dias:
            dias[dia] = {"calorias": 0, "proteina": 0, "carbs": 0, "gordura": 0, "refeicoes": 0, "aderencia": []}
        dias[dia]["calorias"] += r.calorias_estimadas or 0
        dias[dia]["proteina"] += r.proteina_g or 0
        dias[dia]["carbs"] += r.carboidratos_g or 0
        dias[dia]["gordura"] += r.gorduras_g or 0
        dias[dia]["refeicoes"] += 1
        if r.aderencia_percentual:
            dias[dia]["aderencia"].append(r.aderencia_percentual)

    # Calcular média de aderência por dia
    for dia in dias:
        ad = dias[dia]["aderencia"]
        dias[dia]["aderencia_media"] = round(sum(ad) / len(ad)) if ad else None
        del dias[dia]["aderencia"]

    return {"colaborador_id": str(colaborador_id), "periodo": f"{inicio} a {hoje}", "dias": dias}
