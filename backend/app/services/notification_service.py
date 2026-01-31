"""
NutriOffshore - Servico de Notificacoes
Gerencia lembretes e alertas para colaboradores
"""
from datetime import datetime, time
from typing import Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class NotificationType:
    LEMBRETE_REFEICAO = "lembrete_refeicao"
    HIDRATACAO = "hidratacao"
    PESAGEM = "pesagem"
    MOTIVACIONAL = "motivacional"
    ALERTA_MEDICO = "alerta_medico"


MENSAGENS_MOTIVACIONAIS = [
    "Lembre-se: cada refeicao e uma oportunidade de cuidar da sua saude!",
    "Voce esta no caminho certo. Consistencia e mais importante que perfeicao!",
    "Hidratacao e fundamental! Ja bebeu agua nas ultimas 2 horas?",
    "Seu corpo e seu maior patrimonio. Invista nele com boas escolhas alimentares!",
    "Embarque e temporario, mas os habitos saudaveis que voce constroi aqui ficam para sempre.",
    "Nao se compare com ontem dos outros, compare-se com o ontem de voce mesmo.",
    "Faltam poucas horas pro fim do turno. Mantenha o foco na hidratacao!",
    "Proteina em cada refeicao = mais energia e menos fome. Nao esqueca!",
    "Dormir bem e tao importante quanto comer bem. Prepare-se para um bom descanso.",
    "Voce ja registrou suas refeicoes hoje? Acompanhar e o primeiro passo!",
]

LEMBRETES_TURNO_DIURNO = {
    "05:30": "Bom dia! Hora do cafe da manha. Comece com proteina e fibra para manter a energia.",
    "09:30": "Hora do lanche da manha! Uma fruta com castanhas e uma otima opcao.",
    "11:30": "Preparando para o almoco. Lembre-se: comece pela salada!",
    "15:00": "Lanche da tarde! Iogurte natural ou uma fruta para manter o foco.",
    "18:30": "Hora do jantar. Escolha proteina magra e vegetais. Evite frituras a noite.",
    "21:00": "Se sentir fome, uma ceia leve: cha + torrada integral ou fruta.",
}

LEMBRETES_TURNO_NOTURNO = {
    "17:30": "Boa noite de trabalho! Comece com uma refeicao completa e equilibrada.",
    "21:30": "Lanche noturno. Algo leve e nutritivo para manter a energia.",
    "00:00": "Meia-noite! Hora de um lanche proteico. Evite carboidratos simples agora.",
    "03:00": "Madrugada. Hidratacao e essencial! Beba agua ou cha sem acucar.",
    "06:30": "Fim do turno se aproximando. Refeicao leve para preparar para o sono.",
    "07:30": "Hora de descansar. Evite cafeina e refeicoes pesadas antes de dormir.",
}

LEMBRETES_HIDRATACAO = [
    "Hora de beber agua! Mantenha-se hidratado.",
    "Lembrete de hidratacao - um copo de agua agora faz diferenca no seu rendimento!",
    "O ar condicionado da plataforma resseca. Beba agua regularmente!",
]


class NotificationService:
    """Servico de notificacoes e lembretes para colaboradores"""

    @staticmethod
    def gerar_lembretes_diarios(turno: str) -> list[dict]:
        template = LEMBRETES_TURNO_DIURNO if turno == "diurno" else LEMBRETES_TURNO_NOTURNO
        lembretes = []
        for horario, mensagem in template.items():
            lembretes.append({"horario": horario, "mensagem": mensagem, "tipo": NotificationType.LEMBRETE_REFEICAO, "recorrencia": "diaria"})
        horas_hidratacao = ["08:00", "10:00", "12:00", "14:00", "16:00"] if turno == "diurno" else ["20:00", "22:00", "00:00", "02:00", "04:00"]
        for i, hora in enumerate(horas_hidratacao):
            lembretes.append({"horario": hora, "mensagem": LEMBRETES_HIDRATACAO[i % len(LEMBRETES_HIDRATACAO)], "tipo": NotificationType.HIDRATACAO, "recorrencia": "diaria"})
        return lembretes

    @staticmethod
    def gerar_lembrete_pesagem(regime: str) -> dict:
        return {"horario": "06:00", "mensagem": "Dia de pesagem! Va a enfermaria em jejum, antes do cafe. Registre o peso no app.", "tipo": NotificationType.PESAGEM, "recorrencia": "semanal", "dia_semana": "segunda"}

    @staticmethod
    def get_mensagem_motivacional(indice: Optional[int] = None) -> str:
        if indice is not None:
            return MENSAGENS_MOTIVACIONAIS[indice % len(MENSAGENS_MOTIVACIONAIS)]
        import random
        return random.choice(MENSAGENS_MOTIVACIONAIS)

    @staticmethod
    async def criar_alerta_medico(colaborador_id: UUID, tipo: str, motivo: str, recomendacao: str = None) -> dict:
        alerta = {"colaborador_id": str(colaborador_id), "tipo": tipo, "motivo": motivo, "recomendacao": recomendacao, "status": "aberto", "created_at": datetime.utcnow().isoformat()}
        logger.warning(f"ALERTA MEDICO [{tipo.upper()}] - Colaborador {colaborador_id}: {motivo}")
        return alerta

    @staticmethod
    def verificar_alertas_nutricionais(dados_saude: dict) -> list[dict]:
        alertas = []
        glicemia = dados_saude.get("glicemia_jejum")
        if glicemia:
            if glicemia > 126:
                alertas.append({"tipo": "urgente", "motivo": f"Glicemia de jejum elevada: {glicemia} mg/dL (ref: <100)", "recomendacao": "Encaminhar para avaliacao medica. Ajustar plano para baixo indice glicemico."})
            elif glicemia > 100:
                alertas.append({"tipo": "moderado", "motivo": f"Glicemia de jejum alterada: {glicemia} mg/dL (pre-diabetes: 100-125)", "recomendacao": "Monitorar. Reforcar alimentacao com baixo IG e fibras."})
        col_total = dados_saude.get("colesterol_total")
        if col_total and col_total > 240:
            alertas.append({"tipo": "moderado", "motivo": f"Colesterol total elevado: {col_total} mg/dL (ref: <200)", "recomendacao": "Reduzir gordura saturada. Aumentar fibras e omega-3."})
        tg = dados_saude.get("triglicerides")
        if tg and tg > 200:
            alertas.append({"tipo": "moderado", "motivo": f"Triglicerideos elevados: {tg} mg/dL (ref: <150)", "recomendacao": "Reduzir carboidratos simples e acucar. Aumentar omega-3."})
        pa_sis = dados_saude.get("pressao_sistolica")
        pa_dia = dados_saude.get("pressao_diastolica")
        if pa_sis and pa_dia:
            if pa_sis >= 180 or pa_dia >= 120:
                alertas.append({"tipo": "urgente", "motivo": f"Crise hipertensiva: {pa_sis}/{pa_dia} mmHg", "recomendacao": "ENCAMINHAR IMEDIATAMENTE para medico de bordo."})
            elif pa_sis >= 140 or pa_dia >= 90:
                alertas.append({"tipo": "moderado", "motivo": f"Pressao arterial elevada: {pa_sis}/{pa_dia} mmHg", "recomendacao": "Aplicar dieta DASH. Reduzir sodio para <2g/dia."})
        imc = dados_saude.get("imc")
        if imc:
            if imc >= 40:
                alertas.append({"tipo": "urgente", "motivo": f"Obesidade Grau III (IMC: {imc})", "recomendacao": "Acompanhamento medico obrigatorio. Plano nutricional supervisionado."})
            elif imc < 18.5:
                alertas.append({"tipo": "moderado", "motivo": f"Baixo peso (IMC: {imc})", "recomendacao": "Investigar causas. Plano hipercalorico supervisionado."})
        return alertas

