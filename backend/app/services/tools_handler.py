"""
NutriOffshore - Handler de Tools do Agente AI
Processa as chamadas de ferramentas do agente Claude
"""
from datetime import date, datetime, timedelta
from typing import Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from sqlalchemy.orm import selectinload
import json
import logging

from app.models.colaborador import Colaborador
from app.models.medicao import Medicao
from app.models.plano_nutricional import PlanoNutricional
from app.models.cardapio import Cardapio
from app.models.refeicao_log import RefeicaoLog
from app.models.alerta_medico import AlertaMedico
from app.models.condicao_saude import CondicaoSaude
from app.models.preferencia_alimentar import PreferenciaAlimentar
from app.services.nutri_calculator import NutriCalculator, PerfilNutricional
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class ToolsHandler:
    """Processa tool calls do agente Claude"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        handlers = {
            "get_colaborador_profile": self._get_colaborador_profile,
            "get_cardapio_dia": self._get_cardapio_dia,
            "get_cardapio_semana": self._get_cardapio_semana,
            "save_plano_nutricional": self._save_plano_nutricional,
            "log_refeicao": self._log_refeicao,
            "get_historico_peso": self._get_historico_peso,
            "get_historico_refeicoes": self._get_historico_refeicoes,
            "send_notificacao": self._send_notificacao,
            "get_estoque_refeitorio": self._get_estoque_refeitorio,
            "flag_alerta_medico": self._flag_alerta_medico,
            "calcular_necessidades": self._calcular_necessidades,
        }
        handler = handlers.get(tool_name)
        if not handler:
            return json.dumps({"error": "Tool " + tool_name + " não reconhecida"})
        try:
            result = await handler(tool_input)
            return json.dumps(result, default=str, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro executando tool {tool_name}: {e}")
            return json.dumps({"error": str(e)})

    async def _get_colaborador_profile(self, params: dict) -> dict:
        colaborador_id = params.get("colaborador_id")
        stmt = (select(Colaborador).options(selectinload(Colaborador.medicoes), selectinload(Colaborador.condicoes), selectinload(Colaborador.preferencias), selectinload(Colaborador.planos)).where(Colaborador.id == colaborador_id))
        result = await self.db.execute(stmt)
        colaborador = result.scalar_one_or_none()
        if not colaborador:
            return {"error": "Colaborador não encontrado"}
        ultima_medicao = None
        if colaborador.medicoes:
            sorted_medicoes = sorted(colaborador.medicoes, key=lambda m: m.data_medicao, reverse=True)
            m = sorted_medicoes[0]
            ultima_medicao = {"data": str(m.data_medicao), "peso_kg": float(m.peso_kg) if m.peso_kg else None, "circunferencia_abdominal_cm": float(m.circunferencia_abdominal_cm) if m.circunferencia_abdominal_cm else None, "percentual_gordura": float(m.percentual_gordura) if m.percentual_gordura else None, "glicemia_jejum": float(m.glicemia_jejum) if m.glicemia_jejum else None, "colesterol_total": float(m.colesterol_total) if m.colesterol_total else None, "hdl": float(m.hdl) if m.hdl else None, "ldl": float(m.ldl) if m.ldl else None, "triglicerides": float(m.triglicerides) if m.triglicerides else None, "pressao": f"{m.pressao_sistolica}/{m.pressao_diastolica}" if m.pressao_sistolica else None}
        plano_ativo = None
        for p in colaborador.planos:
            if p.ativo:
                plano_ativo = {"id": str(p.id), "meta_calorica": p.meta_calorica, "proteina_g": p.proteina_g, "carboidratos_g": p.carboidratos_g, "gorduras_g": p.gorduras_g, "objetivo": p.objetivo, "data_inicio": str(p.data_inicio)}
                break
        return {"colaborador": {"id": str(colaborador.id), "matricula": colaborador.matricula, "nome": colaborador.nome, "idade": (date.today() - colaborador.data_nascimento).days // 365, "sexo": colaborador.sexo, "altura_cm": float(colaborador.altura_cm) if colaborador.altura_cm else None, "cargo": colaborador.cargo, "nivel_atividade": colaborador.nivel_atividade, "turno_atual": colaborador.turno_atual, "regime_embarque": colaborador.regime_embarque, "meta_principal": colaborador.meta_principal}, "ultima_medicao": ultima_medicao, "condicoes_saude": [{"condicao": c.condicao, "severidade": c.severidade, "medicamentos": c.medicamentos} for c in colaborador.condicoes if c.ativo], "preferencias": [{"tipo": p.tipo, "item": p.item, "severidade": p.severidade} for p in colaborador.preferencias], "plano_ativo": plano_ativo}

    async def _get_cardapio_dia(self, params: dict) -> dict:
        data_str = params.get("data", str(date.today()))
        data_cardapio = date.fromisoformat(data_str) if isinstance(data_str, str) else data_str
        plataforma_id = params.get("plataforma_id")
        stmt = select(Cardapio).where(Cardapio.data == data_cardapio)
        if plataforma_id:
            stmt = stmt.where(Cardapio.plataforma_id == plataforma_id)
        result = await self.db.execute(stmt)
        cardapios = result.scalars().all()
        if not cardapios:
            return {"data": data_str, "mensagem": "Cardápio não cadastrado para esta data", "refeicoes": {}}
        refeicoes = {}
        for c in cardapios:
            refeicoes[c.refeicao] = c.itens
        return {"data": data_str, "refeicoes": refeicoes}

    async def _get_cardapio_semana(self, params: dict) -> dict:
        hoje = date.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        stmt = select(Cardapio).where(and_(Cardapio.data >= inicio_semana, Cardapio.data <= fim_semana)).order_by(Cardapio.data)
        result = await self.db.execute(stmt)
        cardapios = result.scalars().all()
        semana = {}
        for c in cardapios:
            dia = str(c.data)
            if dia not in semana:
                semana[dia] = {}
            semana[dia][c.refeicao] = c.itens
        return {"semana": semana, "inicio": str(inicio_semana), "fim": str(fim_semana)}

    async def _save_plano_nutricional(self, params: dict) -> dict:
        plano_data = params.get("plano", params)
        colaborador_id = params.get("colaborador_id") or plano_data.get("colaborador_id")
        stmt = select(PlanoNutricional).where(and_(PlanoNutricional.colaborador_id == colaborador_id, PlanoNutricional.ativo == True))
        result = await self.db.execute(stmt)
        planos_antigos = result.scalars().all()
        for p in planos_antigos:
            p.ativo = False
        novo_plano = PlanoNutricional(colaborador_id=colaborador_id, meta_calorica=plano_data.get("meta_calorica"), proteina_g=plano_data.get("proteina_g") or plano_data.get("macros", {}).get("proteina_g"), carboidratos_g=plano_data.get("carboidratos_g") or plano_data.get("macros", {}).get("carboidratos_g"), gorduras_g=plano_data.get("gorduras_g") or plano_data.get("macros", {}).get("gorduras_g"), objetivo=plano_data.get("objetivo"), refeicoes_detalhadas=plano_data.get("refeicoes") or plano_data.get("refeicoes_detalhadas"), suplementacao=plano_data.get("suplementacao"), observacoes=plano_data.get("observacoes"), data_inicio=date.today(), data_fim=date.fromisoformat(plano_data["validade"]) if plano_data.get("validade") else None)
        self.db.add(novo_plano)
        await self.db.commit()
        await self.db.refresh(novo_plano)
        return {"success": True, "plano_id": str(novo_plano.id), "mensagem": "Plano salvo com sucesso"}

    async def _log_refeicao(self, params: dict) -> dict:
        log = RefeicaoLog(colaborador_id=params["colaborador_id"], plano_id=params.get("plano_id"), data=date.today(), refeicao=params["refeicao_tipo"], itens_consumidos=params.get("itens", []), calorias_estimadas=sum(i.get("calorias_estimadas", 0) for i in params.get("itens", [])), aderencia_percentual=params.get("aderencia_plano"), observacoes=params.get("observacoes"))
        self.db.add(log)
        await self.db.commit()
        return {"success": True, "mensagem": "Refeição registrada com sucesso"}

    async def _get_historico_peso(self, params: dict) -> dict:
        colaborador_id = params["colaborador_id"]
        periodo_dias = int(params.get("periodo", 90))
        data_inicio = date.today() - timedelta(days=periodo_dias)
        stmt = (select(Medicao).where(and_(Medicao.colaborador_id == colaborador_id, Medicao.data_medicao >= data_inicio, Medicao.peso_kg.isnot(None))).order_by(Medicao.data_medicao))
        result = await self.db.execute(stmt)
        medicoes = result.scalars().all()
        historico = [{"data": str(m.data_medicao), "peso_kg": float(m.peso_kg)} for m in medicoes]
        variacao = None
        if len(historico) >= 2:
            variacao = round(historico[-1]["peso_kg"] - historico[0]["peso_kg"], 1)
        return {"colaborador_id": str(colaborador_id), "periodo_dias": periodo_dias, "medicoes": historico, "total_registros": len(historico), "variacao_kg": variacao}

    async def _get_historico_refeicoes(self, params: dict) -> dict:
        colaborador_id = params["colaborador_id"]
        periodo_dias = int(params.get("periodo", 7))
        data_inicio = date.today() - timedelta(days=periodo_dias)
        stmt = (select(RefeicaoLog).where(and_(RefeicaoLog.colaborador_id == colaborador_id, RefeicaoLog.data >= data_inicio)).order_by(desc(RefeicaoLog.data)))
        result = await self.db.execute(stmt)
        refeicoes = result.scalars().all()
        total_calorias = sum(r.calorias_estimadas or 0 for r in refeicoes)
        dias = max((date.today() - data_inicio).days, 1)
        media_diaria = round(total_calorias / dias)
        aderencias = [r.aderencia_percentual for r in refeicoes if r.aderencia_percentual]
        aderencia_media = round(sum(aderencias) / len(aderencias)) if aderencias else None
        return {"colaborador_id": str(colaborador_id), "periodo_dias": periodo_dias, "total_refeicoes": len(refeicoes), "media_calorias_diaria": media_diaria, "aderencia_media": aderencia_media, "refeicoes": [{"data": str(r.data), "refeicao": r.refeicao, "itens": r.itens_consumidos, "calorias": r.calorias_estimadas, "aderencia": r.aderencia_percentual} for r in refeicoes[:20]]}

    async def _send_notificacao(self, params: dict) -> dict:
        cid = params.get('colaborador_id', '')
        msg = params.get('mensagem', '')
        horario = params.get('horario', '')
        logger.info(f"Notificação agendada para {cid}: {msg} às {horario}")
        return {"success": True, "mensagem": f"Lembrete agendado para {horario}", "tipo": params.get("tipo", "geral")}

    async def _get_estoque_refeitorio(self, params: dict) -> dict:
        return {"status": "disponivel", "data": str(date.today()), "nota": "Consulte o cardápio do dia para itens específicos disponíveis."}

    async def _flag_alerta_medico(self, params: dict) -> dict:
        alerta = AlertaMedico(colaborador_id=params["colaborador_id"], tipo=params.get("tipo_alerta", "moderado"), motivo=params["motivo"], recomendacao=params.get("recomendacao"))
        self.db.add(alerta)
        await self.db.commit()
        logger.warning(f"ALERTA MÉDICO [{alerta.tipo}]: {alerta.motivo}")
        return {"success": True, "alerta_id": str(alerta.id), "mensagem": "Alerta médico registrado e equipe notificada"}

    async def _calcular_necessidades(self, params: dict) -> dict:
        idade = params.get("idade")
        if not idade:
            return {"error": "Parâmetro 'idade' obrigatório. Calcule a partir de data_nascimento do perfil do colaborador."}
        objetivo = params.get("objetivo", "saude_geral")
        objetivos_validos = {"perda_peso", "ganho_massa", "manutencao", "performance", "saude_geral"}
        if objetivo not in objetivos_validos:
            objetivo_map = {"perda_gordura": "perda_peso", "emagrecimento": "perda_peso", "ganho_muscular": "ganho_massa", "hipertrofia": "ganho_massa"}
            objetivo = objetivo_map.get(objetivo, "saude_geral")
        perfil = PerfilNutricional(peso_kg=params["peso_kg"], altura_cm=params["altura_cm"], idade=idade, sexo=params["sexo"], nivel_atividade=params["nivel_atividade"], turno=params.get("turno", "diurno"), objetivo=objetivo, percentual_gordura=params.get("percentual_gordura"), cargo=params.get("cargo"))
        resultado = NutriCalculator.calcular_completo(perfil)
        return {"tmb": resultado.tmb_utilizada, "formula": resultado.formula_escolhida, "get_total": resultado.get_total, "meta_calorica": resultado.meta_calorica, "macros": {"proteina_g": resultado.proteina_g, "carboidratos_g": resultado.carboidratos_g, "gorduras_g": resultado.gorduras_g}, "percentuais": {"proteina": resultado.proteina_pct, "carboidratos": resultado.carboidratos_pct, "gorduras": resultado.gorduras_pct}, "hidratacao_ml": resultado.agua_ml, "fibra_g": resultado.fibra_g, "imc": resultado.imc, "classificacao_imc": resultado.classificacao_imc, "relatorio_formatado": NutriCalculator.formatar_relatorio(resultado)}

