-- NutriOffshore AI - Database Schema
-- Alinhado com os models SQLAlchemy

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Colaboradores (offshore workers)
CREATE TABLE IF NOT EXISTS colaboradores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    altura_cm NUMERIC(5,2),
    cargo VARCHAR(100),
    nivel_atividade VARCHAR(20) DEFAULT 'moderado',
    turno_atual VARCHAR(10) DEFAULT 'diurno',
    regime_embarque VARCHAR(10) DEFAULT '14x14',
    meta_principal VARCHAR(30) DEFAULT 'saude_geral',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medicoes (health measurements)
CREATE TABLE IF NOT EXISTS medicoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    data_medicao DATE NOT NULL,
    peso_kg NUMERIC(5,2),
    circunferencia_abdominal_cm NUMERIC(5,2),
    percentual_gordura NUMERIC(4,2),
    pressao_sistolica INTEGER,
    pressao_diastolica INTEGER,
    glicemia_jejum NUMERIC(5,1),
    colesterol_total NUMERIC(5,1),
    hdl NUMERIC(5,1),
    ldl NUMERIC(5,1),
    triglicerides NUMERIC(5,1),
    fonte VARCHAR(20) DEFAULT 'auto_relato',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Condicoes de Saude (health conditions)
CREATE TABLE IF NOT EXISTS condicoes_saude (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    condicao VARCHAR(50) NOT NULL,
    severidade VARCHAR(20),
    data_diagnostico DATE,
    medicamentos TEXT[],
    observacoes TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Preferencias Alimentares (food preferences - one row per item)
CREATE TABLE IF NOT EXISTS preferencias_alimentares (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    tipo VARCHAR(30) NOT NULL,
    item VARCHAR(100) NOT NULL,
    severidade VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Planos Nutricionais (nutritional plans)
CREATE TABLE IF NOT EXISTS planos_nutricionais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    meta_calorica INTEGER NOT NULL,
    proteina_g INTEGER NOT NULL,
    carboidratos_g INTEGER NOT NULL,
    gorduras_g INTEGER NOT NULL,
    objetivo VARCHAR(30),
    refeicoes_detalhadas JSONB,
    suplementacao JSONB,
    observacoes TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    ativo BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(50) DEFAULT 'nutrioffshore_ai',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cardapios (cafeteria menus)
CREATE TABLE IF NOT EXISTS cardapios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plataforma_id UUID NOT NULL,
    data DATE NOT NULL,
    refeicao VARCHAR(20) NOT NULL,
    itens JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cardapio UNIQUE(plataforma_id, data, refeicao)
);

-- Refeicoes Log (meal logs)
CREATE TABLE IF NOT EXISTS refeicoes_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    plano_id UUID REFERENCES planos_nutricionais(id),
    data DATE NOT NULL,
    refeicao VARCHAR(20) NOT NULL,
    itens_consumidos JSONB NOT NULL,
    calorias_estimadas INTEGER,
    proteina_g INTEGER,
    carboidratos_g INTEGER,
    gorduras_g INTEGER,
    aderencia_percentual INTEGER,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_aderencia CHECK (aderencia_percentual BETWEEN 0 AND 100)
);

-- Alertas Medicos (medical alerts)
CREATE TABLE IF NOT EXISTS alertas_medicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL,
    motivo TEXT NOT NULL,
    recomendacao TEXT,
    status VARCHAR(20) DEFAULT 'aberto',
    visualizado_por VARCHAR(100),
    visualizado_em TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversas do Agente (chat conversations)
CREATE TABLE IF NOT EXISTS conversas_agente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colaborador_id UUID NOT NULL REFERENCES colaboradores(id) ON DELETE CASCADE,
    messages JSONB NOT NULL DEFAULT '[]'::jsonb,
    tokens_utilizados INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_medicoes_colaborador ON medicoes(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_medicoes_data ON medicoes(data_medicao);
CREATE INDEX IF NOT EXISTS idx_condicoes_colaborador ON condicoes_saude(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_preferencias_colaborador ON preferencias_alimentares(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_planos_colaborador ON planos_nutricionais(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_planos_ativo ON planos_nutricionais(ativo);
CREATE INDEX IF NOT EXISTS idx_cardapios_data ON cardapios(data);
CREATE INDEX IF NOT EXISTS idx_cardapios_plataforma ON cardapios(plataforma_id);
CREATE INDEX IF NOT EXISTS idx_refeicoes_colaborador ON refeicoes_log(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_refeicoes_data ON refeicoes_log(data);
CREATE INDEX IF NOT EXISTS idx_alertas_colaborador ON alertas_medicos(colaborador_id);
CREATE INDEX IF NOT EXISTS idx_alertas_status ON alertas_medicos(status);
CREATE INDEX IF NOT EXISTS idx_conversas_colaborador ON conversas_agente(colaborador_id);
