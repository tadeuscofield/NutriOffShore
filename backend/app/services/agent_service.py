"""
NutriOffshore - Servico do Agente AI
Integracao com OpenRouter via OpenAI SDK (modelos gratuitos)
"""
import openai
import json
import logging
from datetime import datetime
from typing import AsyncGenerator, Optional
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.config import get_settings
from app.models.conversa import ConversaAgente
from app.agent.system_prompt import SYSTEM_PROMPT
from app.agent.tools_definition import TOOLS
from app.services.tools_handler import ToolsHandler

logger = logging.getLogger(__name__)
settings = get_settings()


class AgentService:
    """Servico principal do agente NutriOffshore via OpenRouter"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = openai.AsyncOpenAI(
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.tools_handler = ToolsHandler(db)
        self.model = settings.OPENROUTER_MODEL
        self.max_tool_rounds = 8

    def _trim_messages(self, messages: list, max_tokens: int = 12000) -> list:
        """Token-aware sliding window: trims conversation history to stay under max_tokens.

        Always keeps the system message (index 0) and the last user message.
        Estimates tokens as len(text) / 4 per message content.
        Removes oldest non-system messages until total is under limit.
        """
        def estimate_tokens(msg: dict) -> int:
            content = msg.get("content", "") or ""
            # Also count tool_calls arguments if present
            tool_calls = msg.get("tool_calls", [])
            extra = ""
            if tool_calls:
                for tc in tool_calls:
                    func = tc.get("function", {})
                    extra += func.get("arguments", "")
                    extra += func.get("name", "")
            return int((len(content) + len(extra)) / 4)

        total = sum(estimate_tokens(m) for m in messages)
        if total <= max_tokens:
            return messages

        logger.warning(
            f"Trimming conversation history: {total} estimated tokens > {max_tokens} limit, "
            f"{len(messages)} messages"
        )

        # Always keep system message (first) and last user message
        system_msg = messages[0] if messages and messages[0].get("role") == "system" else None
        last_user_idx = None
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                last_user_idx = i
                break

        # Build trimmed list: start removing from oldest non-system messages
        # Keep system + as many recent messages as fit + last user message
        trimmed = []
        if system_msg:
            trimmed.append(system_msg)

        # Work backwards from the end, adding messages until we hit the limit
        reserved_tokens = estimate_tokens(system_msg) if system_msg else 0
        remaining_budget = max_tokens - reserved_tokens

        # Collect messages from newest to oldest (excluding system)
        candidates = messages[1:]  # everything after system
        kept_from_end = []

        for msg in reversed(candidates):
            msg_tokens = estimate_tokens(msg)
            if remaining_budget - msg_tokens >= 0:
                kept_from_end.append(msg)
                remaining_budget -= msg_tokens
            else:
                break

        # Reverse to restore chronological order
        kept_from_end.reverse()

        # Ensure last user message is included
        if last_user_idx is not None:
            last_user_msg = messages[last_user_idx]
            if last_user_msg not in kept_from_end:
                kept_from_end.append(last_user_msg)

        trimmed.extend(kept_from_end)

        logger.info(
            f"Trimmed from {len(messages)} to {len(trimmed)} messages "
            f"(~{sum(estimate_tokens(m) for m in trimmed)} tokens)"
        )
        return trimmed

    async def processar_mensagem(
        self,
        colaborador_id: str,
        mensagem: str,
        conversa_id: Optional[str] = None,
    ) -> dict:
        """Processa mensagem do colaborador e retorna resposta do agente"""

        # Enforce authorization: tool calls can only access this colaborador's data
        self.tools_handler.set_authorized_user(colaborador_id)

        conversa = None
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(colaborador_id=colaborador_id)}
        ]

        if conversa_id:
            conversa = await self._carregar_conversa(conversa_id)
            if conversa and conversa.messages:
                for msg in conversa.messages:
                    messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": mensagem})

        total_tokens = 0
        resposta_final = ""

        for round_num in range(self.max_tool_rounds):
            # Trim messages before each LLM call
            trimmed_messages = self._trim_messages(messages)

            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=8192,
                    messages=trimmed_messages,
                    tools=TOOLS,
                    timeout=60.0,
                    extra_headers={
                        "HTTP-Referer": "https://nutrioffshore.ai",
                        "X-Title": "NutriOffshore AI Agent",
                    },
                )
            except Exception as e:
                logger.error(f"Erro na chamada OpenRouter: {e}")
                raise

            if response.usage:
                total_tokens += (response.usage.prompt_tokens or 0) + (response.usage.completion_tokens or 0)

            choice = response.choices[0]
            assistant_message = choice.message
            logger.info(f"Round {round_num}: finish_reason={choice.finish_reason}, content_len={len(assistant_message.content or '')}, tool_calls={bool(assistant_message.tool_calls)}, content_preview={repr((assistant_message.content or '')[:100])}")

            # Add assistant message to history
            msg_dict = {"role": "assistant", "content": assistant_message.content or ""}
            if assistant_message.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            messages.append(msg_dict)

            if assistant_message.content:
                resposta_final = assistant_message.content

            # If no tool calls, we're done
            if not assistant_message.tool_calls:
                break

            # Execute tool calls
            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    func_args = {}

                logger.info(f"Executando tool: {func_name} com input: {json.dumps(func_args, default=str)[:200]}")
                result = await self.tools_handler.handle_tool_call(func_name, func_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result if isinstance(result, str) else json.dumps(result, default=str, ensure_ascii=False),
                })

        # If we exhausted tool rounds without a text response, force one final call
        if not resposta_final:
            logger.info("No text response after tool rounds, forcing final synthesis call")
            messages.append({"role": "user", "content": "Com base nas informacoes coletadas, responda de forma objetiva e concisa."})

            # Trim before final call
            trimmed_messages = self._trim_messages(messages)

            try:
                final_response = await self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=8192,
                    messages=trimmed_messages,
                    tools=TOOLS,
                    tool_choice="none",
                    timeout=60.0,
                    extra_headers={
                        "HTTP-Referer": "https://nutrioffshore.ai",
                        "X-Title": "NutriOffshore AI Agent",
                    },
                )
                if final_response.usage:
                    total_tokens += (final_response.usage.prompt_tokens or 0) + (final_response.usage.completion_tokens or 0)
                final_content = final_response.choices[0].message.content or ""
                if final_content:
                    resposta_final = final_content
                    messages.append({"role": "assistant", "content": final_content})
            except Exception as e:
                logger.error(f"Erro na chamada final text-only: {e}")

        # Save conversation
        messages_to_save = self._simplificar_mensagens(messages)

        if conversa:
            conversa.messages = messages_to_save
            conversa.tokens_utilizados = (conversa.tokens_utilizados or 0) + total_tokens
            conversa.updated_at = datetime.utcnow()
        else:
            conversa = ConversaAgente(
                id=uuid4(),
                colaborador_id=colaborador_id,
                messages=messages_to_save,
                tokens_utilizados=total_tokens,
            )
            self.db.add(conversa)

        await self.db.commit()

        return {
            "resposta": resposta_final,
            "conversa_id": str(conversa.id),
            "tokens": total_tokens,
        }

    async def processar_mensagem_stream(
        self,
        colaborador_id: str,
        mensagem: str,
        conversa_id: Optional[str] = None,
    ) -> AsyncGenerator[dict, None]:
        """Processa mensagem com streaming de resposta"""

        # Enforce authorization: tool calls can only access this colaborador's data
        self.tools_handler.set_authorized_user(colaborador_id)

        conversa = None
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(colaborador_id=colaborador_id)}
        ]

        if conversa_id:
            conversa = await self._carregar_conversa(conversa_id)
            if conversa and conversa.messages:
                for msg in conversa.messages:
                    messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": mensagem})

        had_text = False
        total_tokens = 0
        try:
            for round_num in range(self.max_tool_rounds):
                collected_text = ""
                collected_tool_calls = {}

                logger.info(f"Stream round {round_num}: calling LLM with {len(messages)} messages")

                # Trim messages before each LLM call
                trimmed_messages = self._trim_messages(messages)

                try:
                    stream = await self.client.chat.completions.create(
                        model=self.model,
                        max_tokens=4096,
                        messages=trimmed_messages,
                        tools=TOOLS,
                        stream=True,
                        timeout=60.0,
                        extra_headers={
                            "HTTP-Referer": "https://nutrioffshore.ai",
                            "X-Title": "NutriOffshore AI Agent",
                        },
                    )
                except Exception as e:
                    logger.error(f"Erro na chamada OpenRouter (stream round {round_num}): {e}")
                    error_msg = "Limite diário atingido. Tente novamente amanhã." if "rate limit" in str(e).lower() or "429" in str(e) else f"Erro ao conectar com a IA: {str(e)[:200]}"
                    yield {"type": "error", "content": error_msg}
                    return

                async for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta

                    # Text content
                    if delta.content:
                        collected_text += delta.content
                        yield {"type": "text", "content": delta.content}

                    # Tool calls (accumulated across chunks)
                    if delta.tool_calls:
                        for tc_delta in delta.tool_calls:
                            idx = tc_delta.index
                            if idx not in collected_tool_calls:
                                collected_tool_calls[idx] = {
                                    "id": tc_delta.id or "",
                                    "name": "",
                                    "arguments": "",
                                }
                            if tc_delta.id:
                                collected_tool_calls[idx]["id"] = tc_delta.id
                            if tc_delta.function:
                                if tc_delta.function.name:
                                    collected_tool_calls[idx]["name"] = tc_delta.function.name
                                if tc_delta.function.arguments:
                                    collected_tool_calls[idx]["arguments"] += tc_delta.function.arguments

                logger.info(f"Stream round {round_num}: text_len={len(collected_text)}, tool_calls={len(collected_tool_calls)}")

                if collected_text:
                    had_text = True

                # Build assistant message
                msg_dict = {"role": "assistant", "content": collected_text}
                if collected_tool_calls:
                    msg_dict["tool_calls"] = [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": tc["arguments"],
                            }
                        }
                        for tc in collected_tool_calls.values()
                    ]
                messages.append(msg_dict)

                if not collected_tool_calls:
                    break

                # Execute tools
                for tc in collected_tool_calls.values():
                    yield {"type": "tool_call", "tool": tc["name"]}
                    try:
                        func_args = json.loads(tc["arguments"])
                    except json.JSONDecodeError:
                        func_args = {}
                    result = await self.tools_handler.handle_tool_call(tc["name"], func_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result if isinstance(result, str) else json.dumps(result, default=str, ensure_ascii=False),
                    })

            # Force synthesis if tools ran but no text was generated
            if not had_text:
                logger.info("Stream: no text after tool rounds, forcing synthesis call")
                messages.append({"role": "user", "content": "Com base nas informações coletadas pelas ferramentas, responda ao pedido do colaborador de forma completa e detalhada."})

                # Trim before synthesis call
                trimmed_messages = self._trim_messages(messages)

                try:
                    stream = await self.client.chat.completions.create(
                        model=self.model,
                        max_tokens=4096,
                        messages=trimmed_messages,
                        stream=True,
                        timeout=60.0,
                        extra_headers={
                            "HTTP-Referer": "https://nutrioffshore.ai",
                            "X-Title": "NutriOffshore AI Agent",
                        },
                    )
                    async for chunk in stream:
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta
                        if delta.content:
                            had_text = True
                            yield {"type": "text", "content": delta.content}
                except Exception as e:
                    logger.error(f"Erro na síntese final streaming: {e}")

            if not had_text:
                yield {"type": "text", "content": "Desculpe, não consegui gerar uma resposta. Por favor, tente novamente com uma pergunta mais simples."}

        except Exception as e:
            logger.error(f"Erro inesperado no streaming: {e}", exc_info=True)
            yield {"type": "error", "content": f"Erro inesperado: {str(e)[:200]}"}

        # Save streaming conversation to database
        try:
            messages_to_save = self._simplificar_mensagens(messages)

            if conversa:
                conversa.messages = messages_to_save
                conversa.tokens_utilizados = (conversa.tokens_utilizados or 0) + total_tokens
                conversa.updated_at = datetime.utcnow()
            else:
                conversa = ConversaAgente(
                    id=uuid4(),
                    colaborador_id=colaborador_id,
                    messages=messages_to_save,
                    tokens_utilizados=total_tokens,
                )
                self.db.add(conversa)

            await self.db.commit()
            yield {"type": "done", "conversa_id": str(conversa.id)}
        except Exception as e:
            logger.error(f"Erro ao salvar conversa streaming: {e}", exc_info=True)

    async def listar_conversas(self, colaborador_id: str, limit: int = 10) -> list:
        """Lista conversas do colaborador"""
        stmt = (
            select(ConversaAgente)
            .where(ConversaAgente.colaborador_id == colaborador_id)
            .order_by(desc(ConversaAgente.updated_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        conversas = result.scalars().all()

        return [
            {
                "id": str(c.id),
                "preview": self._get_preview(c.messages),
                "tokens": c.tokens_utilizados,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            }
            for c in conversas
        ]

    async def buscar_conversa(self, conversa_id: str) -> Optional[dict]:
        """Busca conversa por ID"""
        stmt = select(ConversaAgente).where(ConversaAgente.id == conversa_id)
        result = await self.db.execute(stmt)
        conversa = result.scalar_one_or_none()

        if not conversa:
            return None

        return {
            "id": str(conversa.id),
            "colaborador_id": str(conversa.colaborador_id),
            "messages": conversa.messages,
            "tokens": conversa.tokens_utilizados,
            "created_at": conversa.created_at.isoformat(),
        }

    async def _carregar_conversa(self, conversa_id: str) -> Optional[ConversaAgente]:
        """Carrega conversa do banco"""
        stmt = select(ConversaAgente).where(ConversaAgente.id == conversa_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def _simplificar_mensagens(messages: list) -> list:
        """Simplifica mensagens para armazenamento (remove system prompt e tool details)"""
        simplified = []
        for msg in messages:
            role = msg.get("role", "")
            if role == "system":
                continue
            if role == "tool":
                continue
            if role == "user":
                simplified.append({"role": "user", "content": msg.get("content", "")})
            elif role == "assistant":
                content = msg.get("content", "")
                if content:
                    simplified.append({"role": "assistant", "content": content})
        return simplified

    @staticmethod
    def _get_preview(messages: list) -> str:
        """Gera preview da conversa"""
        if not messages:
            return "Conversa vazia"
        first_user = next((m["content"] for m in messages if m.get("role") == "user"), "")
        if isinstance(first_user, str):
            return first_user[:100]
        return "Conversa"
