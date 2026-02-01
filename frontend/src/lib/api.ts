import type {
  Colaborador,
  ColaboradorCreate,
  ColaboradorUpdate,
  Medicao,
  MedicaoCreate,
  PlanoNutricional,
  PlanoNutricionalUpdate,
  ChatResponse,
  ChatStreamChunk,
  Conversa,
  ConversaDetail,
  CardapioDia,
  CardapioSemana,
  Refeicao,
  ResumoDiario,
  AlertaMedico,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Performs a fetch with an AbortController-based timeout.
 * Non-streaming requests default to 30s; streaming uses a longer timeout.
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeoutMs = 30000
): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    return res;
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit,
  timeoutMs = 30000
): Promise<T> {
  const res = await fetchWithTimeout(
    `${API_BASE}${endpoint}`,
    {
      headers: { "Content-Type": "application/json", ...options?.headers },
      ...options,
    },
    timeoutMs
  );
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Erro na API");
  }
  return res.json();
}

export const api = {
  // Colaboradores
  listarColaboradores: (): Promise<Colaborador[]> =>
    fetchAPI<Colaborador[]>("/api/v1/colaboradores/"),

  buscarColaborador: (id: string): Promise<Colaborador> =>
    fetchAPI<Colaborador>(`/api/v1/colaboradores/${id}`),

  criarColaborador: (data: ColaboradorCreate): Promise<Colaborador> =>
    fetchAPI<Colaborador>("/api/v1/colaboradores/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  atualizarColaborador: (id: string, data: ColaboradorUpdate): Promise<Colaborador> =>
    fetchAPI<Colaborador>(`/api/v1/colaboradores/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  registrarMedicao: (id: string, data: MedicaoCreate): Promise<Medicao> =>
    fetchAPI<Medicao>(`/api/v1/colaboradores/${id}/medicoes`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listarMedicoes: (colaboradorId: string): Promise<Medicao[]> =>
    fetchAPI<Medicao[]>(`/api/v1/colaboradores/${colaboradorId}/medicoes`),

  // Planos
  planoAtivo: (colaboradorId: string): Promise<PlanoNutricional> =>
    fetchAPI<PlanoNutricional>(`/api/v1/planos/colaborador/${colaboradorId}/ativo`),

  listarPlanos: (colaboradorId: string): Promise<PlanoNutricional[]> =>
    fetchAPI<PlanoNutricional[]>(`/api/v1/planos/colaborador/${colaboradorId}`),

  atualizarPlano: (planoId: string, data: PlanoNutricionalUpdate): Promise<PlanoNutricional> =>
    fetchAPI<PlanoNutricional>(`/api/v1/planos/${planoId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  deletarPlano: async (planoId: string): Promise<void> => {
    const res = await fetchWithTimeout(
      `${API_BASE}/api/v1/planos/${planoId}`,
      { method: "DELETE" }
    );
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(error.detail || "Erro ao deletar plano");
    }
  },

  // Cardapios
  cardapioDia: (data: string): Promise<CardapioDia> =>
    fetchAPI<CardapioDia>(`/api/v1/cardapios/dia/${data}`),

  cardapioSemana: (): Promise<CardapioSemana> =>
    fetchAPI<CardapioSemana>("/api/v1/cardapios/semana"),

  // Refeicoes
  refeicoesdia: (colaboradorId: string, data: string): Promise<Refeicao[]> =>
    fetchAPI<Refeicao[]>(`/api/v1/refeicoes/colaborador/${colaboradorId}/dia/${data}`),

  listarRefeicoes: (colaboradorId: string): Promise<ResumoDiario[]> =>
    fetchAPI<ResumoDiario[]>(`/api/v1/refeicoes/colaborador/${colaboradorId}/resumo-semanal`),

  resumoSemanal: (colaboradorId: string): Promise<ResumoDiario[]> =>
    fetchAPI<ResumoDiario[]>(`/api/v1/refeicoes/colaborador/${colaboradorId}/resumo-semanal`),

  // Chat
  enviarMensagem: (
    colaboradorId: string,
    mensagem: string,
    conversaId?: string
  ): Promise<ChatResponse> =>
    fetchAPI<ChatResponse>(
      "/api/v1/chat/mensagem",
      {
        method: "POST",
        body: JSON.stringify({
          colaborador_id: colaboradorId,
          mensagem,
          conversa_id: conversaId,
        }),
      },
      60000 // 60s timeout for chat completions
    ),

  historicoConversas: (colaboradorId: string): Promise<Conversa[]> =>
    fetchAPI<Conversa[]>(`/api/v1/chat/historico/${colaboradorId}`),

  buscarConversa: (conversaId: string): Promise<ConversaDetail> =>
    fetchAPI<ConversaDetail>(`/api/v1/chat/conversa/${conversaId}`),

  // Chat Streaming (120s timeout, AbortController signal passed through)
  enviarMensagemStream: async function* (
    colaboradorId: string,
    mensagem: string,
    conversaId?: string
  ): AsyncGenerator<ChatStreamChunk, void, unknown> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 120000);

    try {
      const res = await fetch(`${API_BASE}/api/v1/chat/mensagem/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          colaborador_id: colaboradorId,
          mensagem,
          conversa_id: conversaId,
        }),
        signal: controller.signal,
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) return;

      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") return;
            try {
              yield JSON.parse(data) as ChatStreamChunk;
            } catch {
              // skip malformed chunks
            }
          }
        }
      }
    } finally {
      clearTimeout(timeout);
    }
  },

  // Alertas
  listarAlertas: (status?: string): Promise<AlertaMedico[]> =>
    fetchAPI<AlertaMedico[]>(`/api/v1/alertas/?status=${status || "aberto"}`),

  listarAlertasColaborador: (
    colaboradorId: string,
    status?: string
  ): Promise<AlertaMedico[]> =>
    fetchAPI<AlertaMedico[]>(
      `/api/v1/alertas/colaborador/${colaboradorId}?status=${status || "aberto"}`
    ),
};
