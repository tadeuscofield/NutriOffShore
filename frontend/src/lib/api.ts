const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Erro na API");
  }
  return res.json();
}

// Colaboradores
export const api = {
  // Colaboradores
  listarColaboradores: () => fetchAPI<any[]>("/api/v1/colaboradores/"),
  buscarColaborador: (id: string) => fetchAPI<any>(`/api/v1/colaboradores/${id}`),
  criarColaborador: (data: any) =>
    fetchAPI<any>("/api/v1/colaboradores/", { method: "POST", body: JSON.stringify(data) }),
  atualizarColaborador: (id: string, data: any) =>
    fetchAPI<any>(`/api/v1/colaboradores/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  registrarMedicao: (id: string, data: any) =>
    fetchAPI<any>(`/api/v1/colaboradores/${id}/medicoes`, { method: "POST", body: JSON.stringify(data) }),

  // Planos
  planoAtivo: (colaboradorId: string) =>
    fetchAPI<any>(`/api/v1/planos/colaborador/${colaboradorId}/ativo`),
  listarPlanos: (colaboradorId: string) =>
    fetchAPI<any[]>(`/api/v1/planos/colaborador/${colaboradorId}`),
  atualizarPlano: (planoId: string, data: any) =>
    fetchAPI<any>(`/api/v1/planos/${planoId}`, { method: "PUT", body: JSON.stringify(data) }),
  deletarPlano: async (planoId: string) => {
    const res = await fetch(`${API_BASE}/api/v1/planos/${planoId}`, { method: "DELETE" });
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(error.detail || "Erro ao deletar plano");
    }
  },

  // Cardápios
  cardapioDia: (data: string) => fetchAPI<any>(`/api/v1/cardapios/dia/${data}`),
  cardapioSemana: () => fetchAPI<any>("/api/v1/cardapios/semana"),

  // Refeições
  refeicoesdia: (colaboradorId: string, data: string) =>
    fetchAPI<any>(`/api/v1/refeicoes/colaborador/${colaboradorId}/dia/${data}`),
  resumoSemanal: (colaboradorId: string) =>
    fetchAPI<any>(`/api/v1/refeicoes/colaborador/${colaboradorId}/resumo-semanal`),

  // Chat
  enviarMensagem: (colaboradorId: string, mensagem: string, conversaId?: string) =>
    fetchAPI<{ resposta: string; conversa_id: string; tokens_utilizados?: number }>(
      "/api/v1/chat/mensagem",
      {
        method: "POST",
        body: JSON.stringify({ colaborador_id: colaboradorId, mensagem, conversa_id: conversaId }),
      }
    ),
  historicoConversas: (colaboradorId: string) =>
    fetchAPI<any[]>(`/api/v1/chat/historico/${colaboradorId}`),

  // Chat Streaming
  enviarMensagemStream: async function* (
    colaboradorId: string,
    mensagem: string,
    conversaId?: string
  ) {
    const res = await fetch(`${API_BASE}/api/v1/chat/mensagem/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ colaborador_id: colaboradorId, mensagem, conversa_id: conversaId }),
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
            yield JSON.parse(data);
          } catch {}
        }
      }
    }
  },

  // Alertas
  listarAlertas: (status?: string) =>
    fetchAPI<any[]>(`/api/v1/alertas/?status=${status || "aberto"}`),
};
