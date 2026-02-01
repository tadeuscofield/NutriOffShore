export interface Colaborador {
  id: string;
  matricula: string;
  nome: string;
  data_nascimento: string;
  sexo: "M" | "F";
  altura_cm: number | null;
  cargo: string | null;
  nivel_atividade: string;
  turno_atual: string;
  regime_embarque: string;
  meta_principal: string;
}

export interface ColaboradorCreate {
  matricula: string;
  nome: string;
  data_nascimento: string;
  sexo: "M" | "F";
  altura_cm?: number | null;
  cargo?: string | null;
  nivel_atividade?: string;
  turno_atual?: string;
  regime_embarque?: string;
  meta_principal?: string;
}

export interface ColaboradorUpdate {
  nome?: string;
  altura_cm?: number | null;
  cargo?: string | null;
  nivel_atividade?: string;
  turno_atual?: string;
  regime_embarque?: string;
  meta_principal?: string;
}

export interface Medicao {
  data_medicao: string;
  peso_kg: number | null;
  circunferencia_abdominal_cm: number | null;
  percentual_gordura: number | null;
  glicemia_jejum: number | null;
  colesterol_total: number | null;
  hdl: number | null;
  ldl: number | null;
  triglicerides: number | null;
  pressao_sistolica: number | null;
  pressao_diastolica: number | null;
}

export interface MedicaoCreate {
  data_medicao: string;
  peso_kg?: number | null;
  circunferencia_abdominal_cm?: number | null;
  percentual_gordura?: number | null;
  glicemia_jejum?: number | null;
  colesterol_total?: number | null;
  hdl?: number | null;
  ldl?: number | null;
  triglicerides?: number | null;
  pressao_sistolica?: number | null;
  pressao_diastolica?: number | null;
}

export interface PlanoNutricional {
  id: string;
  colaborador_id: string;
  meta_calorica: number;
  proteina_g: number;
  carboidratos_g: number;
  gorduras_g: number;
  objetivo: string | null;
  refeicoes_detalhadas: any;
  observacoes: string | null;
  ativo: boolean;
  data_inicio: string;
  data_fim: string | null;
  created_by: string;
  created_at: string;
}

export interface PlanoNutricionalUpdate {
  meta_calorica?: number;
  proteina_g?: number;
  carboidratos_g?: number;
  gorduras_g?: number;
  objetivo?: string | null;
  ativo?: boolean;
  data_fim?: string | null;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface ChatResponse {
  resposta: string;
  conversa_id: string;
  tokens_utilizados?: number;
}

export interface ChatStreamChunk {
  type: "text" | "error" | "tool_call" | "done";
  content?: string;
  tool?: string;
  conversa_id?: string;
}

export interface Conversa {
  id: string;
  preview: string;
  tokens?: number;
  created_at: string;
  updated_at?: string | null;
}

export interface ConversaDetail {
  id: string;
  colaborador_id: string;
  messages: ChatMessage[];
  tokens: number;
  created_at: string;
}

export interface ResumoDiario {
  data: string;
  total_calorias: number;
  total_proteina_g: number;
  total_carboidratos_g: number;
  total_gorduras_g: number;
  refeicoes_registradas: number;
  aderencia_media: number | null;
}

export interface ItemCardapio {
  item: string;
  categoria: string;
  calorias_porcao: number | null;
  proteina_g: number | null;
  carb_g: number | null;
  gordura_g: number | null;
  indice_glicemico: string | null;
}

export interface CardapioDia {
  data: string;
  itens: ItemCardapio[];
}

export interface CardapioSemana {
  semana: string;
  dias: CardapioDia[];
}

export interface Refeicao {
  id: string;
  colaborador_id: string;
  data: string;
  tipo: string;
  itens: string[];
  calorias_total: number | null;
  aderencia: number | null;
}

export interface AlertaMedico {
  id: string;
  colaborador_id: string;
  tipo: "urgente" | "moderado" | "baixo";
  motivo: string;
  recomendacao: string | null;
  status: string;
  created_at: string;
}
