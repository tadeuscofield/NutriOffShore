"""
NutriOffshore - Servico de Calculos Nutricionais
Implementa todas as formulas de TMB, GET e distribuicao de macronutrientes
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import math


class Sexo(str, Enum):
    MASCULINO = "M"
    FEMININO = "F"


class NivelAtividade(str, Enum):
    SEDENTARIO = "sedentario"
    LEVE = "leve"
    MODERADO = "moderado"
    INTENSO = "intenso"


class Turno(str, Enum):
    DIURNO = "diurno"
    NOTURNO = "noturno"


class Objetivo(str, Enum):
    PERDA_PESO = "perda_peso"
    GANHO_MASSA = "ganho_massa"
    MANUTENCAO = "manutencao"
    PERFORMANCE = "performance"
    SAUDE_GERAL = "saude_geral"


FATORES_ATIVIDADE = {
    "sedentario": 1.2,
    "leve": 1.375,
    "moderado": 1.55,
    "intenso": 1.725,
}

AJUSTE_NEAT_FUNCAO = {
    "administrativo": 0,
    "supervisor": 50,
    "tecnico_seguranca": 80,
    "operador_producao": 150,
    "tecnico_manutencao": 200,
    "eletricista": 180,
    "mecanico": 220,
    "soldador": 250,
    "plataformista": 300,
    "guindasteiro": 180,
    "cozinheiro": 120,
    "camareiro": 150,
}


@dataclass
class PerfilNutricional:
    peso_kg: float
    altura_cm: float
    idade: int
    sexo: str
    nivel_atividade: str
    turno: str = "diurno"
    objetivo: str = "saude_geral"
    percentual_gordura: Optional[float] = None
    cargo: Optional[str] = None


@dataclass
class ResultadoCalculo:
    tmb_harris_benedict: float
    tmb_mifflin: float
    tmb_katch_mcardle: Optional[float]
    tmb_utilizada: float
    formula_escolhida: str
    fator_atividade: float
    ajuste_turno_noturno: float
    efeito_termico_alimentos: float
    ajuste_neat: float
    get_total: float
    meta_calorica: float
    deficit_superavit: float
    proteina_g: float
    carboidratos_g: float
    gorduras_g: float
    proteina_kcal: float
    carboidratos_kcal: float
    gorduras_kcal: float
    proteina_pct: float
    carboidratos_pct: float
    gorduras_pct: float
    agua_ml: int
    fibra_g: int
    imc: float
    classificacao_imc: str


class NutriCalculator:
    """Calculadora nutricional completa para contexto offshore"""

    @staticmethod
    def calcular_imc(peso_kg: float, altura_cm: float) -> tuple[float, str]:
        if altura_cm <= 0:
            raise ValueError("Altura deve ser maior que zero para calcular o IMC")
        if peso_kg <= 0:
            raise ValueError("Peso deve ser maior que zero para calcular o IMC")
        altura_m = altura_cm / 100
        imc = peso_kg / (altura_m ** 2)
        if imc < 18.5:
            classificacao = "Abaixo do peso"
        elif imc < 25:
            classificacao = "Peso normal"
        elif imc < 30:
            classificacao = "Sobrepeso"
        elif imc < 35:
            classificacao = "Obesidade Grau I"
        elif imc < 40:
            classificacao = "Obesidade Grau II"
        else:
            classificacao = "Obesidade Grau III"
        return round(imc, 1), classificacao

    @staticmethod
    def tmb_harris_benedict(peso_kg: float, altura_cm: float, idade: int, sexo: str) -> float:
        """Formula de Harris-Benedict Revisada (1984)"""
        if sexo == "M":
            tmb = 88.362 + (13.397 * peso_kg) + (4.799 * altura_cm) - (5.677 * idade)
        else:
            tmb = 447.593 + (9.247 * peso_kg) + (3.098 * altura_cm) - (4.330 * idade)
        return round(tmb, 0)

    @staticmethod
    def tmb_mifflin_st_jeor(peso_kg: float, altura_cm: float, idade: int, sexo: str) -> float:
        """Formula de Mifflin-St Jeor (1990) - considerada mais precisa"""
        if sexo == "M":
            tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * idade) + 5
        else:
            tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * idade) - 161
        return round(tmb, 0)

    @staticmethod
    def tmb_katch_mcardle(peso_kg: float, percentual_gordura: float) -> float:
        """Formula de Katch-McArdle - usa massa magra"""
        massa_magra = peso_kg * (1 - percentual_gordura / 100)
        tmb = 370 + (21.6 * massa_magra)
        return round(tmb, 0)

    @staticmethod
    def escolher_melhor_tmb(perfil: PerfilNutricional) -> tuple[float, str]:
        if perfil.percentual_gordura and perfil.percentual_gordura > 0:
            tmb = NutriCalculator.tmb_katch_mcardle(perfil.peso_kg, perfil.percentual_gordura)
            return tmb, "Katch-McArdle (massa magra disponivel)"
        else:
            tmb = NutriCalculator.tmb_mifflin_st_jeor(perfil.peso_kg, perfil.altura_cm, perfil.idade, perfil.sexo)
            return tmb, "Mifflin-St Jeor (padrao-ouro sem composicao corporal)"

    @staticmethod
    def calcular_get(tmb: float, nivel_atividade: str, turno: str, cargo: Optional[str] = None) -> dict:
        fator = FATORES_ATIVIDADE.get(nivel_atividade, 1.55)
        get_base = tmb * fator
        ajuste_noturno = 0
        if turno == "noturno":
            ajuste_noturno = -(get_base * 0.07)
        tef = get_base * 0.10
        neat = 0
        if cargo and cargo.lower() in AJUSTE_NEAT_FUNCAO:
            neat = AJUSTE_NEAT_FUNCAO[cargo.lower()]
        get_total = get_base + ajuste_noturno + tef + neat
        return {"get_base": round(get_base, 0), "fator_atividade": fator, "ajuste_noturno": round(ajuste_noturno, 0), "tef": round(tef, 0), "neat": neat, "get_total": round(get_total, 0)}

    @staticmethod
    def calcular_meta_calorica(get_total: float, objetivo: str) -> tuple[float, float]:
        ajustes = {"perda_peso": -400, "ganho_massa": 250, "manutencao": 0, "performance": 100, "saude_geral": 0}
        ajuste = ajustes.get(objetivo, 0)
        meta = max(get_total + ajuste, 1200)
        return round(meta, 0), ajuste

    @staticmethod
    def distribuir_macros(meta_calorica: float, peso_kg: float, objetivo: str, condicoes: list[str] = None) -> dict:
        condicoes = condicoes or []
        if objetivo in ("ganho_massa", "performance"):
            proteina_por_kg = 2.0
        elif objetivo == "perda_peso":
            proteina_por_kg = 2.2
        else:
            proteina_por_kg = 1.6
        proteina_g = round(peso_kg * proteina_por_kg)
        proteina_kcal = proteina_g * 4
        gordura_por_kg = 0.8 if "dislipidemia" in condicoes else 1.0
        gordura_g = round(peso_kg * gordura_por_kg)
        gordura_kcal = gordura_g * 9
        carb_kcal = meta_calorica - proteina_kcal - gordura_kcal
        carb_g = round(max(carb_kcal / 4, 50))
        carb_kcal = carb_g * 4
        if "diabetes_tipo2" in condicoes:
            reducao_carb = round(carb_g * 0.20)
            carb_g -= reducao_carb
            gordura_g += round(reducao_carb * 4 / 9)
            carb_kcal = carb_g * 4
            gordura_kcal = gordura_g * 9
        total_kcal = proteina_kcal + carb_kcal + gordura_kcal
        return {"proteina_g": proteina_g, "carboidratos_g": carb_g, "gorduras_g": gordura_g, "proteina_kcal": proteina_kcal, "carboidratos_kcal": carb_kcal, "gorduras_kcal": gordura_kcal, "proteina_pct": round(proteina_kcal / total_kcal * 100, 1), "carboidratos_pct": round(carb_kcal / total_kcal * 100, 1), "gorduras_pct": round(gordura_kcal / total_kcal * 100, 1)}

    @staticmethod
    def calcular_hidratacao(peso_kg: float, nivel_atividade: str, turno: str) -> int:
        base = peso_kg * 35
        ajustes = {"sedentario": 0, "leve": 300, "moderado": 500, "intenso": 800}
        agua = base + ajustes.get(nivel_atividade, 300) + 200
        if turno == "noturno":
            agua += 100
        return round(agua / 50) * 50

    @staticmethod
    def calcular_fibra(meta_calorica: float, condicoes: list[str] = None) -> int:
        condicoes = condicoes or []
        base = max(25, round(meta_calorica / 1000 * 14))
        if "diabetes_tipo2" in condicoes:
            base = max(base, 30)
        return min(base, 40)

    @classmethod
    def calcular_completo(cls, perfil: PerfilNutricional, condicoes: list[str] = None) -> ResultadoCalculo:
        condicoes = condicoes or []
        imc, classificacao_imc = cls.calcular_imc(perfil.peso_kg, perfil.altura_cm)
        tmb_hb = cls.tmb_harris_benedict(perfil.peso_kg, perfil.altura_cm, perfil.idade, perfil.sexo)
        tmb_mifflin = cls.tmb_mifflin_st_jeor(perfil.peso_kg, perfil.altura_cm, perfil.idade, perfil.sexo)
        tmb_katch = None
        if perfil.percentual_gordura:
            tmb_katch = cls.tmb_katch_mcardle(perfil.peso_kg, perfil.percentual_gordura)
        tmb_escolhida, formula = cls.escolher_melhor_tmb(perfil)
        get_info = cls.calcular_get(tmb_escolhida, perfil.nivel_atividade, perfil.turno, perfil.cargo)
        meta, deficit_superavit = cls.calcular_meta_calorica(get_info["get_total"], perfil.objetivo)
        macros = cls.distribuir_macros(meta, perfil.peso_kg, perfil.objetivo, condicoes)
        agua = cls.calcular_hidratacao(perfil.peso_kg, perfil.nivel_atividade, perfil.turno)
        fibra = cls.calcular_fibra(meta, condicoes)
        return ResultadoCalculo(
            tmb_harris_benedict=tmb_hb, tmb_mifflin=tmb_mifflin, tmb_katch_mcardle=tmb_katch,
            tmb_utilizada=tmb_escolhida, formula_escolhida=formula,
            fator_atividade=get_info["fator_atividade"], ajuste_turno_noturno=get_info["ajuste_noturno"],
            efeito_termico_alimentos=get_info["tef"], ajuste_neat=get_info["neat"],
            get_total=get_info["get_total"], meta_calorica=meta, deficit_superavit=deficit_superavit,
            proteina_g=macros["proteina_g"], carboidratos_g=macros["carboidratos_g"],
            gorduras_g=macros["gorduras_g"], proteina_kcal=macros["proteina_kcal"],
            carboidratos_kcal=macros["carboidratos_kcal"], gorduras_kcal=macros["gorduras_kcal"],
            proteina_pct=macros["proteina_pct"], carboidratos_pct=macros["carboidratos_pct"],
            gorduras_pct=macros["gorduras_pct"], agua_ml=agua, fibra_g=fibra,
            imc=imc, classificacao_imc=classificacao_imc,
        )

    @classmethod
    def formatar_relatorio(cls, resultado: "ResultadoCalculo", nome: str = "Colaborador") -> str:
        """Formata resultado em texto legivel para o chat"""
        lines = []
        lines.append(f"Avaliacao Nutricional - {nome}")
        lines.append("")
        lines.append("Dados Antropometricos:")
        lines.append(f"* IMC: {resultado.imc} - {resultado.classificacao_imc}")
        lines.append("")
        lines.append("Taxa Metabolica Basal (TMB):")
        lines.append(f"* Harris-Benedict: {resultado.tmb_harris_benedict:.0f} kcal")
        lines.append(f"* Mifflin-St Jeor: {resultado.tmb_mifflin:.0f} kcal")
        if resultado.tmb_katch_mcardle:
            lines.append(f"* Katch-McArdle: {resultado.tmb_katch_mcardle:.0f} kcal")
        lines.append(f"* Utilizada: {resultado.tmb_utilizada:.0f} kcal ({resultado.formula_escolhida})")
        lines.append("")
        lines.append("Gasto Energetico Total (GET):")
        lines.append(f"* TMB x Fator ({resultado.fator_atividade}): base")
        lines.append(f"* Ajuste turno noturno: {resultado.ajuste_turno_noturno:+.0f} kcal")
        lines.append(f"* Efeito termico alimentos: +{resultado.efeito_termico_alimentos:.0f} kcal")
        lines.append(f"* NEAT ocupacional: +{resultado.ajuste_neat:.0f} kcal")
        lines.append(f"* GET Total: {resultado.get_total:.0f} kcal")
        lines.append("")
        lines.append(f"Meta Calorica: {resultado.meta_calorica:.0f} kcal/dia ({resultado.deficit_superavit:+.0f} kcal)")
        lines.append("")
        lines.append("Distribuicao de Macronutrientes:")
        lines.append(f"* Proteina: {resultado.proteina_g}g ({resultado.proteina_pct}%) = {resultado.proteina_kcal:.0f} kcal")
        lines.append(f"* Carboidratos: {resultado.carboidratos_g}g ({resultado.carboidratos_pct}%) = {resultado.carboidratos_kcal:.0f} kcal")
        lines.append(f"* Gorduras: {resultado.gorduras_g}g ({resultado.gorduras_pct}%) = {resultado.gorduras_kcal:.0f} kcal")
        lines.append("")
        lines.append(f"Hidratacao: {resultado.agua_ml} ml/dia")
        lines.append(f"Fibra: {resultado.fibra_g}g/dia")
        return chr(10).join(lines)
