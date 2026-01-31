-- NutriOffshore AI - Seed Data
-- 3 test collaborators with menus and meal logs
-- Aligned with SQLAlchemy models

DO $$
DECLARE
    plataforma_demo UUID := 'a0000000-0000-0000-0000-000000000001';
    colab1_id UUID;
    colab2_id UUID;
    colab3_id UUID;
    plano1_id UUID;
    plano2_id UUID;
    plano3_id UUID;
BEGIN

-- =============================================
-- COLABORADOR 1: Carlos Silva - Operador de Guindastes
-- =============================================
INSERT INTO colaboradores (id, matricula, nome, data_nascimento, sexo, altura_cm, cargo, nivel_atividade, turno_atual, regime_embarque, meta_principal)
VALUES (uuid_generate_v4(), 'MAT-001', 'Carlos Silva', '1990-03-15', 'M', 178.00, 'Operador de Guindastes', 'intenso', 'diurno', '14x14', 'perda_gordura')
RETURNING id INTO colab1_id;

INSERT INTO medicoes (colaborador_id, data_medicao, peso_kg, percentual_gordura, circunferencia_abdominal_cm, pressao_sistolica, pressao_diastolica, glicemia_jejum, colesterol_total, hdl, ldl, triglicerides, fonte)
VALUES
    (colab1_id, CURRENT_DATE - INTERVAL '30 days', 95.00, 24.00, 98.0, 135, 88, 102, 210, 42, 140, 180, 'auto_relato'),
    (colab1_id, CURRENT_DATE - INTERVAL '15 days', 93.50, 23.00, 96.5, 130, 85, 98, 200, 44, 130, 165, 'auto_relato'),
    (colab1_id, CURRENT_DATE, 92.50, 22.00, 95.0, 128, 82, 95, 195, 46, 125, 155, 'auto_relato');

INSERT INTO condicoes_saude (colaborador_id, condicao, severidade, data_diagnostico, medicamentos, observacoes, ativo)
VALUES
    (colab1_id, 'Colesterol Alto', 'leve', '2024-06-01', ARRAY['Controle dietético'], 'Hipercolesterolemia leve, em tratamento dietético', TRUE);

INSERT INTO preferencias_alimentares (colaborador_id, tipo, item, severidade) VALUES
    (colab1_id, 'preferencia', 'Frango grelhado', NULL),
    (colab1_id, 'preferencia', 'Arroz integral', NULL),
    (colab1_id, 'preferencia', 'Saladas', NULL),
    (colab1_id, 'restricao', 'Frituras', 'moderada'),
    (colab1_id, 'aversao', 'Camarão', NULL),
    (colab1_id, 'aversao', 'Feijoada', NULL);

INSERT INTO planos_nutricionais (id, colaborador_id, meta_calorica, proteina_g, carboidratos_g, gorduras_g, objetivo, refeicoes_detalhadas, data_inicio, ativo, created_by)
VALUES (uuid_generate_v4(), colab1_id, 2800, 175, 350, 93, 'perda_gordura',
    '{"cafe_manha": {"horario": "06:00", "itens": ["Ovos mexidos (3)", "Pão integral (2 fatias)", "Fruta", "Café sem açúcar"], "calorias": 550},
      "lanche_manha": {"horario": "09:30", "itens": ["Iogurte natural", "Granola (30g)", "Banana"], "calorias": 300},
      "almoco": {"horario": "12:00", "itens": ["Arroz integral (150g)", "Frango grelhado (200g)", "Salada verde", "Feijão (100g)", "Legumes refogados"], "calorias": 750},
      "lanche_tarde": {"horario": "15:30", "itens": ["Fruta", "Castanhas (30g)"], "calorias": 250},
      "jantar": {"horario": "19:00", "itens": ["Peixe grelhado (200g)", "Batata doce (150g)", "Salada", "Legumes"], "calorias": 650},
      "ceia": {"horario": "21:30", "itens": ["Whey protein (1 scoop)", "Leite desnatado"], "calorias": 300}}'::jsonb,
    CURRENT_DATE - INTERVAL '15 days', TRUE, 'nutrioffshore_ai')
RETURNING id INTO plano1_id;

-- =============================================
-- COLABORADOR 2: Ana Rodrigues - Engenheira de Processos
-- =============================================
INSERT INTO colaboradores (id, matricula, nome, data_nascimento, sexo, altura_cm, cargo, nivel_atividade, turno_atual, regime_embarque, meta_principal)
VALUES (uuid_generate_v4(), 'MAT-002', 'Ana Rodrigues', '1996-07-22', 'F', 165.00, 'Engenheira de Processos', 'leve', 'diurno', '14x14', 'manutencao')
RETURNING id INTO colab2_id;

INSERT INTO medicoes (colaborador_id, data_medicao, peso_kg, percentual_gordura, pressao_sistolica, pressao_diastolica, glicemia_jejum, fonte)
VALUES
    (colab2_id, CURRENT_DATE - INTERVAL '30 days', 64.00, 28.00, 110, 70, 88, 'auto_relato'),
    (colab2_id, CURRENT_DATE - INTERVAL '15 days', 63.00, 27.00, 108, 68, 85, 'auto_relato'),
    (colab2_id, CURRENT_DATE, 62.00, 26.00, 105, 65, 82, 'auto_relato');

INSERT INTO condicoes_saude (colaborador_id, condicao, severidade, medicamentos, observacoes, ativo)
VALUES
    (colab2_id, 'Intolerância à Lactose', 'leve', ARRAY['Lactase quando necessário'], 'Tolera pequenas quantidades de derivados', TRUE);

INSERT INTO preferencias_alimentares (colaborador_id, tipo, item, severidade) VALUES
    (colab2_id, 'intolerancia', 'Lactose', 'leve'),
    (colab2_id, 'preferencia', 'Salmão', NULL),
    (colab2_id, 'preferencia', 'Quinoa', NULL),
    (colab2_id, 'preferencia', 'Frutas vermelhas', NULL),
    (colab2_id, 'restricao', 'Leite puro', 'moderada'),
    (colab2_id, 'restricao', 'Queijos fortes', 'leve');

INSERT INTO planos_nutricionais (id, colaborador_id, meta_calorica, proteina_g, carboidratos_g, gorduras_g, objetivo, refeicoes_detalhadas, data_inicio, ativo, created_by)
VALUES (uuid_generate_v4(), colab2_id, 1900, 95, 237, 63, 'manutencao',
    '{"cafe_manha": {"horario": "06:30", "itens": ["Tapioca com ovo (2)", "Fruta", "Café sem açúcar"], "calorias": 380},
      "lanche_manha": {"horario": "09:30", "itens": ["Mix de castanhas (30g)", "Fruta"], "calorias": 200},
      "almoco": {"horario": "12:00", "itens": ["Arroz (120g)", "Peixe grelhado (150g)", "Salada variada", "Lentilha (80g)"], "calorias": 550},
      "lanche_tarde": {"horario": "15:30", "itens": ["Iogurte sem lactose", "Granola (20g)"], "calorias": 180},
      "jantar": {"horario": "19:00", "itens": ["Sopa de legumes com frango", "Torrada integral (2)"], "calorias": 420},
      "ceia": {"horario": "21:00", "itens": ["Chá de camomila", "Fruta"], "calorias": 170}}'::jsonb,
    CURRENT_DATE - INTERVAL '10 days', TRUE, 'nutrioffshore_ai')
RETURNING id INTO plano2_id;

-- =============================================
-- COLABORADOR 3: Roberto Santos - Mergulhador
-- =============================================
INSERT INTO colaboradores (id, matricula, nome, data_nascimento, sexo, altura_cm, cargo, nivel_atividade, turno_atual, regime_embarque, meta_principal)
VALUES (uuid_generate_v4(), 'MAT-003', 'Roberto Santos', '1983-11-08', 'M', 182.00, 'Mergulhador', 'muito_intenso', 'noturno', '14x14', 'performance')
RETURNING id INTO colab3_id;

INSERT INTO medicoes (colaborador_id, data_medicao, peso_kg, percentual_gordura, pressao_sistolica, pressao_diastolica, glicemia_jejum, colesterol_total, hdl, ldl, triglicerides, fonte)
VALUES
    (colab3_id, CURRENT_DATE - INTERVAL '30 days', 84.00, 14.50, 120, 75, 90, 175, 55, 100, 120, 'auto_relato'),
    (colab3_id, CURRENT_DATE - INTERVAL '15 days', 84.50, 14.80, 118, 74, 88, 170, 56, 98, 115, 'auto_relato'),
    (colab3_id, CURRENT_DATE, 85.00, 15.00, 122, 76, 92, 172, 54, 102, 118, 'auto_relato');

INSERT INTO condicoes_saude (colaborador_id, condicao, severidade, medicamentos, observacoes, ativo)
VALUES
    (colab3_id, 'Pré-diabetes', 'moderado', ARRAY['Metformina 500mg'], 'Pré-diabetes controlado com dieta e medicação', TRUE);

INSERT INTO preferencias_alimentares (colaborador_id, tipo, item, severidade) VALUES
    (colab3_id, 'alergia', 'Amendoim', 'grave'),
    (colab3_id, 'preferencia', 'Carnes magras', NULL),
    (colab3_id, 'preferencia', 'Peixes', NULL),
    (colab3_id, 'preferencia', 'Ovos', NULL),
    (colab3_id, 'restricao', 'Doces', 'moderada'),
    (colab3_id, 'restricao', 'Refrigerantes', 'grave');

INSERT INTO planos_nutricionais (id, colaborador_id, meta_calorica, proteina_g, carboidratos_g, gorduras_g, objetivo, refeicoes_detalhadas, suplementacao, data_inicio, ativo, created_by)
VALUES (uuid_generate_v4(), colab3_id, 3200, 200, 380, 107, 'performance',
    '{"cafe_manha": {"horario": "19:00", "itens": ["Ovos (4)", "Aveia (60g)", "Banana", "Café"], "calorias": 650},
      "lanche_1": {"horario": "22:00", "itens": ["Shake proteico", "Pão integral com peito de peru"], "calorias": 400},
      "almoco_noturno": {"horario": "01:00", "itens": ["Arroz integral (200g)", "Carne magra (250g)", "Feijão (120g)", "Salada", "Legumes"], "calorias": 900},
      "lanche_2": {"horario": "04:00", "itens": ["Fruta", "Castanhas (40g)", "Iogurte natural"], "calorias": 350},
      "jantar_noturno": {"horario": "07:00", "itens": ["Peixe (200g)", "Batata doce (200g)", "Vegetais grelhados"], "calorias": 650},
      "ceia": {"horario": "10:00", "itens": ["Caseína (1 scoop)", "Fruta"], "calorias": 250}}'::jsonb,
    '{"items": [{"nome": "Whey Protein", "dose": "30g pós-mergulho", "horario": "Após atividade"}, {"nome": "Creatina", "dose": "5g/dia", "horario": "Manhã"}, {"nome": "Vitamina D3", "dose": "2000UI", "horario": "Com refeição"}]}'::jsonb,
    CURRENT_DATE - INTERVAL '20 days', TRUE, 'nutrioffshore_ai')
RETURNING id INTO plano3_id;

-- =============================================
-- CARDAPIOS DA PLATAFORMA (menus do dia)
-- =============================================
INSERT INTO cardapios (plataforma_id, data, refeicao, itens) VALUES
(plataforma_demo, CURRENT_DATE, 'cafe_manha', '[
    {"item": "Ovos mexidos", "categoria": "proteina", "calorias_porcao": 180, "proteina_g": 14, "carb_g": 2, "gordura_g": 12},
    {"item": "Pão integral", "categoria": "carboidrato", "calorias_porcao": 130, "proteina_g": 5, "carb_g": 24, "gordura_g": 2},
    {"item": "Pão francês", "categoria": "carboidrato", "calorias_porcao": 150, "proteina_g": 4, "carb_g": 30, "gordura_g": 1},
    {"item": "Tapioca", "categoria": "carboidrato", "calorias_porcao": 120, "proteina_g": 0, "carb_g": 28, "gordura_g": 0},
    {"item": "Frutas variadas", "categoria": "fruta", "calorias_porcao": 80, "proteina_g": 1, "carb_g": 20, "gordura_g": 0},
    {"item": "Iogurte natural", "categoria": "laticinio", "calorias_porcao": 90, "proteina_g": 6, "carb_g": 8, "gordura_g": 4},
    {"item": "Granola", "categoria": "cereal", "calorias_porcao": 140, "proteina_g": 3, "carb_g": 22, "gordura_g": 5},
    {"item": "Café", "categoria": "bebida", "calorias_porcao": 5, "proteina_g": 0, "carb_g": 0, "gordura_g": 0}
]'::jsonb),

(plataforma_demo, CURRENT_DATE, 'almoco', '[
    {"item": "Arroz branco", "categoria": "carboidrato", "calorias_porcao": 200, "proteina_g": 4, "carb_g": 44, "gordura_g": 0, "indice_glicemico": "alto"},
    {"item": "Arroz integral", "categoria": "carboidrato", "calorias_porcao": 180, "proteina_g": 4, "carb_g": 38, "gordura_g": 2, "indice_glicemico": "medio"},
    {"item": "Feijão carioca", "categoria": "leguminosa", "calorias_porcao": 150, "proteina_g": 9, "carb_g": 25, "gordura_g": 1, "indice_glicemico": "baixo"},
    {"item": "Frango grelhado", "categoria": "proteina", "calorias_porcao": 220, "proteina_g": 35, "carb_g": 0, "gordura_g": 8},
    {"item": "Peixe assado", "categoria": "proteina", "calorias_porcao": 200, "proteina_g": 30, "carb_g": 0, "gordura_g": 8},
    {"item": "Bife acebolado", "categoria": "proteina", "calorias_porcao": 280, "proteina_g": 28, "carb_g": 5, "gordura_g": 16},
    {"item": "Salada verde", "categoria": "vegetal", "calorias_porcao": 25, "proteina_g": 2, "carb_g": 4, "gordura_g": 0},
    {"item": "Batata doce", "categoria": "carboidrato", "calorias_porcao": 160, "proteina_g": 2, "carb_g": 37, "gordura_g": 0, "indice_glicemico": "medio"},
    {"item": "Legumes refogados", "categoria": "vegetal", "calorias_porcao": 80, "proteina_g": 3, "carb_g": 12, "gordura_g": 3},
    {"item": "Sobremesa - Fruta", "categoria": "fruta", "calorias_porcao": 70, "proteina_g": 1, "carb_g": 18, "gordura_g": 0}
]'::jsonb),

(plataforma_demo, CURRENT_DATE, 'jantar', '[
    {"item": "Sopa de legumes com frango", "categoria": "prato_completo", "calorias_porcao": 250, "proteina_g": 18, "carb_g": 28, "gordura_g": 6},
    {"item": "Macarrão integral com molho", "categoria": "carboidrato", "calorias_porcao": 320, "proteina_g": 12, "carb_g": 52, "gordura_g": 8},
    {"item": "Omelete de legumes", "categoria": "proteina", "calorias_porcao": 200, "proteina_g": 16, "carb_g": 4, "gordura_g": 14},
    {"item": "Salada completa", "categoria": "vegetal", "calorias_porcao": 120, "proteina_g": 6, "carb_g": 15, "gordura_g": 4},
    {"item": "Pão integral", "categoria": "carboidrato", "calorias_porcao": 130, "proteina_g": 5, "carb_g": 24, "gordura_g": 2},
    {"item": "Fruta da estação", "categoria": "fruta", "calorias_porcao": 70, "proteina_g": 1, "carb_g": 18, "gordura_g": 0}
]'::jsonb);

-- =============================================
-- REFEICAO LOGS (últimos 2 dias para Carlos)
-- =============================================
INSERT INTO refeicoes_log (colaborador_id, plano_id, data, refeicao, itens_consumidos, calorias_estimadas, proteina_g, carboidratos_g, gorduras_g, aderencia_percentual) VALUES
(colab1_id, plano1_id, CURRENT_DATE - INTERVAL '2 days', 'cafe_manha',
    '[{"alimento": "Ovos mexidos (3)", "quantidade": "180g", "calorias_estimadas": 270}, {"alimento": "Pão integral (2)", "quantidade": "80g", "calorias_estimadas": 200}, {"alimento": "Café sem açúcar", "quantidade": "200ml", "calorias_estimadas": 5}]'::jsonb,
    475, 28, 40, 20, 85),

(colab1_id, plano1_id, CURRENT_DATE - INTERVAL '2 days', 'almoco',
    '[{"alimento": "Arroz integral", "quantidade": "150g", "calorias_estimadas": 180}, {"alimento": "Frango grelhado", "quantidade": "200g", "calorias_estimadas": 330}, {"alimento": "Feijão", "quantidade": "100g", "calorias_estimadas": 100}, {"alimento": "Salada verde", "quantidade": "100g", "calorias_estimadas": 25}]'::jsonb,
    635, 48, 55, 12, 90),

(colab1_id, plano1_id, CURRENT_DATE - INTERVAL '1 day', 'cafe_manha',
    '[{"alimento": "Ovos cozidos (3)", "quantidade": "150g", "calorias_estimadas": 210}, {"alimento": "Tapioca", "quantidade": "80g", "calorias_estimadas": 120}, {"alimento": "Banana", "quantidade": "1 unidade", "calorias_estimadas": 90}]'::jsonb,
    420, 22, 48, 10, 75),

(colab1_id, plano1_id, CURRENT_DATE - INTERVAL '1 day', 'almoco',
    '[{"alimento": "Arroz branco", "quantidade": "200g", "calorias_estimadas": 260}, {"alimento": "Bife acebolado", "quantidade": "180g", "calorias_estimadas": 280}, {"alimento": "Feijão", "quantidade": "120g", "calorias_estimadas": 120}, {"alimento": "Batata frita", "quantidade": "100g", "calorias_estimadas": 270}]'::jsonb,
    930, 35, 80, 35, 55);

-- =============================================
-- ALERTAS demo
-- =============================================
INSERT INTO alertas_medicos (colaborador_id, tipo, motivo, recomendacao, status)
VALUES
    (colab1_id, 'colesterol', 'Colesterol total de 210mg/dL acima do recomendado (200mg/dL).', 'Reforçar dieta com baixo teor de gordura saturada. Priorizar peixes, azeite e fibras.', 'aberto'),
    (colab3_id, 'glicemia', 'Glicemia de 92mg/dL dentro do limite, mas paciente pré-diabético.', 'Manter acompanhamento e dieta de baixo índice glicêmico. Evitar açúcares refinados.', 'aberto');

-- =============================================
-- CONVERSA demo para Carlos
-- =============================================
INSERT INTO conversas_agente (colaborador_id, messages, tokens_utilizados) VALUES
(colab1_id,
    '[{"role": "user", "content": "Olá, preciso de ajuda com minha alimentação aqui na plataforma. Sou operador de guindaste e tenho colesterol alto."},
      {"role": "assistant", "content": "Olá Carlos! Sou a NutriOffshore AI, sua nutricionista virtual. Vi que você é operador de guindastes, trabalho bastante intenso! Vamos criar um plano personalizado para você, considerando seu colesterol alto e a necessidade de manter energia para suas atividades."},
      {"role": "assistant", "content": "Com base no seu perfil (92.5kg, 178cm, atividade intensa), calculei suas necessidades:\n\n- Gasto energético total: ~2800 kcal/dia\n- Proteína: 175g (25%)\n- Carboidratos: 350g (50%)\n- Gorduras: 93g (30%) - com foco em gorduras boas\n\nPara o colesterol, vamos priorizar: peixes, azeite, fibras e reduzir frituras."}]'::jsonb,
    1250);

END $$;
