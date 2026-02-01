"""Rotas de Chat com Agente AI NutriOffshore"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import json
import logging

from app.database import get_db
from app.auth import get_current_user
from app.services.agent_service import AgentService
from app.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    colaborador_id: UUID
    mensagem: str
    conversa_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    resposta: str
    conversa_id: str
    tokens_utilizados: Optional[int] = None


def _verify_colaborador_ownership(data: ChatMessage, current_user: dict) -> None:
    """Verifica se o colaborador_id da mensagem pertence ao usuario autenticado."""
    if current_user.get("auth_disabled"):
        return
    if str(data.colaborador_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Acesso negado: colaborador_id nao corresponde ao usuario autenticado")


@router.post("/mensagem", response_model=ChatResponse)
@limiter.limit("10/minute")
async def enviar_mensagem(
    request: Request,
    data: ChatMessage,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Envia mensagem para o agente NutriOffshore e recebe resposta"""
    _verify_colaborador_ownership(data, current_user)
    try:
        agent = AgentService(db)
        resultado = await agent.processar_mensagem(
            colaborador_id=str(data.colaborador_id),
            mensagem=data.mensagem,
            conversa_id=str(data.conversa_id) if data.conversa_id else None,
        )
        return ChatResponse(
            resposta=resultado["resposta"],
            conversa_id=resultado["conversa_id"],
            tokens_utilizados=resultado.get("tokens"),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao processar mensagem")


@router.post("/mensagem/stream")
@limiter.limit("10/minute")
async def enviar_mensagem_stream(
    request: Request,
    data: ChatMessage,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Envia mensagem com resposta em streaming"""
    _verify_colaborador_ownership(data, current_user)
    agent = AgentService(db)

    async def generate():
        try:
            async for chunk in agent.processar_mensagem_stream(
                colaborador_id=str(data.colaborador_id),
                mensagem=data.mensagem,
                conversa_id=str(data.conversa_id) if data.conversa_id else None,
            ):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.error(f"Erro no streaming: {e}", exc_info=True)
            error_payload = {"type": "error", "content": "Erro interno ao processar mensagem"}
            yield f"data: {json.dumps(error_payload, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/historico/{colaborador_id}")
@limiter.limit("60/minute")
async def historico_conversas(
    request: Request,
    colaborador_id: UUID,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Lista conversas anteriores do colaborador"""
    if not current_user.get("auth_disabled") and str(colaborador_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    agent = AgentService(db)
    return await agent.listar_conversas(str(colaborador_id), limit)


@router.get("/conversa/{conversa_id}")
@limiter.limit("60/minute")
async def buscar_conversa(
    request: Request,
    conversa_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Busca uma conversa específica"""
    agent = AgentService(db)
    conversa = await agent.buscar_conversa(str(conversa_id))
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conversa
