"""Definicao das Tools do Agente NutriOffshore - formato OpenAI (compativel OpenRouter)"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_colaborador_profile",
            "description": "Busca perfil completo do colaborador incluindo medicoes, condicoes de saude e preferencias alimentares",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {
                        "type": "string",
                        "description": "ID do colaborador (UUID)"
                    }
                },
                "required": ["colaborador_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cardapio_dia",
            "description": "Retorna cardapio do refeitorio da plataforma para um dia especifico",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Data no formato YYYY-MM-DD"
                    },
                    "plataforma_id": {
                        "type": "string",
                        "description": "ID da plataforma (UUID). Padrao: a0000000-0000-0000-0000-000000000001"
                    }
                },
                "required": ["data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cardapio_semana",
            "description": "Retorna cardapios da semana inteira da plataforma",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_plano_nutricional",
            "description": "Salva um plano nutricional personalizado para o colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "meta_calorica": {"type": "number", "description": "Meta calorica diaria em kcal"},
                    "proteina_g": {"type": "number", "description": "Gramas de proteina por dia"},
                    "carboidratos_g": {"type": "number", "description": "Gramas de carboidratos por dia"},
                    "gorduras_g": {"type": "number", "description": "Gramas de gorduras por dia"},
                    "objetivo": {"type": "string", "description": "Objetivo do plano"},
                    "refeicoes": {"type": "array", "description": "Detalhamento das refeicoes"},
                    "suplementacao": {"type": "array", "description": "Suplementos recomendados"},
                    "observacoes": {"type": "string"}
                },
                "required": ["colaborador_id", "meta_calorica", "proteina_g", "carboidratos_g", "gorduras_g"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_refeicao",
            "description": "Registra uma refeicao consumida pelo colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "refeicao_tipo": {
                        "type": "string",
                        "enum": ["cafe_manha", "lanche_manha", "almoco", "lanche_tarde", "jantar", "ceia"],
                        "description": "Tipo da refeicao"
                    },
                    "itens": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "alimento": {"type": "string"},
                                "quantidade": {"type": "string"},
                                "calorias_estimadas": {"type": "number"}
                            }
                        },
                        "description": "Itens consumidos"
                    },
                    "aderencia_plano": {"type": "number", "description": "0-100 aderencia ao plano"},
                    "observacoes": {"type": "string"}
                },
                "required": ["colaborador_id", "refeicao_tipo", "itens"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historico_peso",
            "description": "Busca evolucao de peso e medicoes do colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "periodo": {"type": "number", "description": "Periodo em dias (padrao: 90)"}
                },
                "required": ["colaborador_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historico_refeicoes",
            "description": "Busca historico de refeicoes registradas",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "periodo": {"type": "number", "description": "Periodo em dias (padrao: 7)"}
                },
                "required": ["colaborador_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notificacao",
            "description": "Agenda notificacao ou lembrete para o colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "mensagem": {"type": "string", "description": "Texto da notificacao (max 200 chars)"},
                    "horario": {"type": "string", "description": "Horario no formato HH:MM"},
                    "tipo": {
                        "type": "string",
                        "enum": ["lembrete_refeicao", "hidratacao", "pesagem", "motivacional"]
                    },
                    "recorrencia": {
                        "type": "string",
                        "enum": ["unica", "diaria", "semanal"]
                    }
                },
                "required": ["colaborador_id", "mensagem", "horario", "tipo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_estoque_refeitorio",
            "description": "Consulta disponibilidade de itens no refeitorio da plataforma",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flag_alerta_medico",
            "description": "Sinaliza situacao que requer atencao do medico de bordo",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "tipo_alerta": {
                        "type": "string",
                        "enum": ["urgente", "moderado", "baixo"]
                    },
                    "motivo": {"type": "string", "description": "Descricao do motivo do alerta"},
                    "recomendacao": {"type": "string", "description": "Recomendacao para equipe medica"}
                },
                "required": ["colaborador_id", "tipo_alerta", "motivo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_necessidades",
            "description": "Calcula TMB, GET e necessidades de macronutrientes para o colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "peso_kg": {"type": "number"},
                    "altura_cm": {"type": "number"},
                    "idade": {"type": "number"},
                    "sexo": {"type": "string", "enum": ["M", "F"]},
                    "nivel_atividade": {"type": "string", "enum": ["sedentario", "leve", "moderado", "intenso"]},
                    "turno": {"type": "string", "enum": ["diurno", "noturno"]},
                    "objetivo": {"type": "string", "enum": ["perda_peso", "ganho_massa", "manutencao", "performance", "saude_geral"]},
                    "percentual_gordura": {"type": "number"},
                    "cargo": {"type": "string"}
                },
                "required": ["peso_kg", "altura_cm", "idade", "sexo", "nivel_atividade", "objetivo"]
            }
        }
    }
]
