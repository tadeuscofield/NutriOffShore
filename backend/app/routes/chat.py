"""Rotas de Chat com Agente AI NutriOffshore"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import json
import logging

from app.database import get_db
from app.services.agent_service import AgentService

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


@router.post("/mensagem", response_model=ChatResponse)
async def enviar_mensagem(data: ChatMessage, db: AsyncSession = Depends(get_db)):
    """Envia mensagem para o agente NutriOffshore e recebe resposta"""
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
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")


@router.post("/mensagem/stream")
async def enviar_mensagem_stream(data: ChatMessage, db: AsyncSession = Depends(get_db)):
    """Envia mensagem com resposta em streaming"""
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
            error_payload = {"type": "error", "content": f"Erro no servidor: {str(e)[:200]}"}
            yield f"data: {json.dumps(error_payload, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/historico/{colaborador_id}")
async def historico_conversas(colaborador_id: UUID, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Lista conversas anteriores do colaborador"""
    agent = AgentService(db)
    return await agent.listar_conversas(str(colaborador_id), limit)


@router.get("/conversa/{conversa_id}")
async def buscar_conversa(conversa_id: UUID, db: AsyncSession = Depends(get_db)):
    """Busca uma conversa específica"""
    agent = AgentService(db)
    conversa = await agent.buscar_conversa(str(conversa_id))
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conversa
