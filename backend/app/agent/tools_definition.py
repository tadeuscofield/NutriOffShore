"""Definição das Tools do Agente NutriOffshore - formato OpenAI (compatível OpenRouter)"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_colaborador_profile",
            "description": "Busca perfil completo do colaborador incluindo medições, condições de saúde e preferências alimentares",
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
            "description": "Retorna cardápio do refeitório da plataforma para um dia específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Data no formato YYYY-MM-DD"
                    },
                    "plataforma_id": {
                        "type": "string",
                        "description": "ID da plataforma (UUID). Padrão: a0000000-0000-0000-0000-000000000001"
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
            "description": "Retorna cardápios da semana inteira da plataforma",
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
                    "meta_calorica": {"type": "number", "description": "Meta calórica diária em kcal"},
                    "proteina_g": {"type": "number", "description": "Gramas de proteína por dia"},
                    "carboidratos_g": {"type": "number", "description": "Gramas de carboidratos por dia"},
                    "gorduras_g": {"type": "number", "description": "Gramas de gorduras por dia"},
                    "objetivo": {"type": "string", "description": "Objetivo do plano"},
                    "refeicoes": {"type": "array", "description": "Detalhamento das refeições"},
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
            "description": "Registra uma refeição consumida pelo colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "refeicao_tipo": {
                        "type": "string",
                        "enum": ["cafe_manha", "lanche_manha", "almoco", "lanche_tarde", "jantar", "ceia"],
                        "description": "Tipo da refeição"
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
                    "aderencia_plano": {"type": "number", "description": "0-100 aderência ao plano"},
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
            "description": "Busca evolução de peso e medições do colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "periodo": {"type": "number", "description": "Período em dias (padrão: 90)"}
                },
                "required": ["colaborador_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historico_refeicoes",
            "description": "Busca histórico de refeições registradas",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "periodo": {"type": "number", "description": "Período em dias (padrão: 7)"}
                },
                "required": ["colaborador_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notificacao",
            "description": "Agenda notificação ou lembrete para o colaborador",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "mensagem": {"type": "string", "description": "Texto da notificação (max 200 chars)"},
                    "horario": {"type": "string", "description": "Horário no formato HH:MM"},
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
            "description": "Consulta disponibilidade de itens no refeitório da plataforma",
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
            "description": "Sinaliza situação que requer atenção do médico de bordo",
            "parameters": {
                "type": "object",
                "properties": {
                    "colaborador_id": {"type": "string"},
                    "tipo_alerta": {
                        "type": "string",
                        "enum": ["urgente", "moderado", "baixo"]
                    },
                    "motivo": {"type": "string", "description": "Descrição do motivo do alerta"},
                    "recomendacao": {"type": "string", "description": "Recomendação para equipe médica"}
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
