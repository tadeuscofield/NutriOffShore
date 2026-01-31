"use client";
import { useState, useEffect } from "react";
import Header from "@/components/Header";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";

interface Plano {
  id: string;
  meta_calorica: number;
  proteina_g: number;
  carboidratos_g: number;
  gorduras_g: number;
  objetivo: string | null;
  refeicoes_detalhadas: any;
  observacoes: string | null;
  data_inicio: string;
  data_fim: string | null;
  ativo: boolean;
  created_by: string;
  created_at: string;
}

const refeicoesPadrao = [
  { nome: "Café da manhã", horario: "06:00", pct: 0.23, desc: "Proteína + carboidrato integral + fruta" },
  { nome: "Lanche manhã", horario: "09:30", pct: 0.09, desc: "Fruta com castanhas ou iogurte" },
  { nome: "Almoço", horario: "12:00", pct: 0.31, desc: "Proteína magra + arroz/batata + salada abundante" },
  { nome: "Lanche tarde", horario: "15:30", pct: 0.09, desc: "Iogurte natural ou fruta + proteína" },
  { nome: "Jantar", horario: "19:00", pct: 0.24, desc: "Proteína + legumes + carb moderado" },
  { nome: "Ceia", horario: "21:00", pct: 0.04, desc: "Chá + 1 torrada integral (se necessário)" },
];

export default function PlanoPage() {
  const { colaboradorId, colaborador } = useAppStore();
  const [plano, setPlano] = useState<Plano | null>(null);
  const [planos, setPlanos] = useState<Plano[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editForm, setEditForm] = useState({ meta_calorica: 0, proteina_g: 0, carboidratos_g: 0, gorduras_g: 0, objetivo: "" });
  const [showConfirmDelete, setShowConfirmDelete] = useState<string | null>(null);
  const [message, setMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  useEffect(() => {
    if (!colaboradorId) {
      setLoading(false);
      return;
    }
    loadPlanos();
  }, [colaboradorId]);

  async function loadPlanos() {
    setLoading(true);
    try {
      const list = await api.listarPlanos(colaboradorId!);
      setPlanos(list);
      const ativo = list.find((p: Plano) => p.ativo);
      setPlano(ativo || list[0] || null);
    } catch {
      setPlano(null);
      setPlanos([]);
    } finally {
      setLoading(false);
    }
  }

  function startEdit() {
    if (!plano) return;
    setEditForm({
      meta_calorica: plano.meta_calorica,
      proteina_g: plano.proteina_g,
      carboidratos_g: plano.carboidratos_g,
      gorduras_g: plano.gorduras_g,
      objetivo: plano.objetivo || "",
    });
    setEditing(true);
  }

  async function saveEdit() {
    if (!plano) return;
    try {
      const updated = await api.atualizarPlano(plano.id, editForm);
      setPlano(updated);
      setPlanos(prev => prev.map(p => p.id === updated.id ? updated : p));
      setEditing(false);
      setMessage({ text: "Plano atualizado com sucesso!", type: "success" });
      setTimeout(() => setMessage(null), 3000);
    } catch (err) {
      setMessage({ text: err instanceof Error ? err.message : "Erro ao salvar", type: "error" });
    }
  }

  async function deletePlano(id: string) {
    try {
      await api.deletarPlano(id);
      setShowConfirmDelete(null);
      setMessage({ text: "Plano excluído com sucesso!", type: "success" });
      setTimeout(() => setMessage(null), 3000);
      await loadPlanos();
    } catch (err) {
      setMessage({ text: err instanceof Error ? err.message : "Erro ao excluir", type: "error" });
    }
  }

  function downloadPlano() {
    if (!plano) return;
    const refeicoes = plano.refeicoes_detalhadas || refeicoesPadrao.map(r => ({
      ...r, cal: Math.round(plano.meta_calorica * r.pct),
    }));

    const nome = colaborador?.nome || "Colaborador";
    const lines = [
      "===================================================",
      "       PLANO NUTRICIONAL - NutriOffshore AI",
      "===================================================",
      "",
      `Colaborador: ${nome}`,
      `Data de início: ${new Date(plano.data_inicio).toLocaleDateString("pt-BR")}`,
      `Objetivo: ${plano.objetivo || "Não definido"}`,
      `Status: ${plano.ativo ? "Ativo" : "Inativo"}`,
      "",
      "--- METAS DIÁRIAS ---------------------------------",
      `  Calorias:      ${plano.meta_calorica} kcal`,
      `  Proteína:      ${plano.proteina_g}g`,
      `  Carboidratos:  ${plano.carboidratos_g}g`,
      `  Gorduras:      ${plano.gorduras_g}g`,
      "",
      "--- DISTRIBUIÇÃO DE REFEIÇÕES ----------------------",
      ...refeicoes.map((r: any) =>
        `  ${r.horario || ""}  ${r.nome} (${r.cal || "—"} kcal)\n       ${r.desc || ""}`
      ),
      "",
    ];
    if (plano.observacoes) {
      lines.push("--- OBSERVAÇÕES -----------------------------------");
      lines.push(`  ${plano.observacoes}`);
      lines.push("");
    }
    lines.push(`Gerado por: ${plano.created_by} em ${new Date(plano.created_at).toLocaleDateString("pt-BR")}`);
    lines.push("===================================================");

    const txt = lines.join("\n");
    const blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `plano_nutricional_${nome.replace(/\s+/g, "_")}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  if (!colaboradorId) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Header />
        <main className="max-w-4xl mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold text-slate-800 mb-6">Plano Nutricional</h2>
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
            <div className="text-4xl mb-3">📋</div>
            <p className="text-slate-500">Selecione um colaborador na aba <strong>Chat</strong> para ver o plano nutricional.</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-800">Plano Nutricional</h2>
          {colaborador && (
            <span className="text-sm text-ocean-600 bg-ocean-50 px-3 py-1 rounded-lg">
              {colaborador.nome}
            </span>
          )}
        </div>

        {/* Messages */}
        {message && (
          <div className={`mb-4 p-3 rounded-lg text-sm ${message.type === "success" ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"}`}>
            {message.text}
          </div>
        )}

        {loading ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
            <div className="animate-pulse text-slate-400">Carregando plano...</div>
          </div>
        ) : !plano ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
            <div className="text-4xl mb-3">📋</div>
            <p className="text-slate-500 mb-2">Nenhum plano nutricional encontrado.</p>
            <p className="text-sm text-slate-400">Peça ao agente IA no <strong>Chat</strong> para montar seu plano.</p>
          </div>
        ) : (
          <>
            {/* Active Plan Card */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <h3 className="font-semibold text-slate-800">
                    {editing ? "Editando Plano" : "Plano Ativo"}
                  </h3>
                  <span className={`text-xs px-3 py-1 rounded-full font-medium ${plano.ativo ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-500"}`}>
                    {plano.ativo ? "Ativo" : "Inativo"}
                  </span>
                </div>
                <div className="flex gap-2">
                  {!editing ? (
                    <>
                      <button onClick={downloadPlano} title="Baixar plano" className="p-2 text-slate-400 hover:text-ocean-600 hover:bg-ocean-50 rounded-lg transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                      </button>
                      <button onClick={startEdit} title="Editar plano" className="p-2 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                      </button>
                      <button onClick={() => setShowConfirmDelete(plano.id)} title="Excluir plano" className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                      </button>
                    </>
                  ) : (
                    <>
                      <button onClick={saveEdit} className="px-4 py-2 bg-ocean-600 text-white text-sm rounded-lg hover:bg-ocean-500 transition-colors">
                        Salvar
                      </button>
                      <button onClick={() => setEditing(false)} className="px-4 py-2 text-slate-500 text-sm rounded-lg hover:bg-slate-100 transition-colors">
                        Cancelar
                      </button>
                    </>
                  )}
                </div>
              </div>

              {/* Macros Grid */}
              {editing ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-3 bg-orange-50 rounded-xl">
                    <input type="number" value={editForm.meta_calorica} onChange={e => setEditForm(f => ({ ...f, meta_calorica: Number(e.target.value) }))} className="w-full text-center text-2xl font-bold text-orange-600 bg-transparent border-b border-orange-300 focus:outline-none" />
                    <div className="text-xs text-orange-500 mt-1">kcal/dia</div>
                  </div>
                  <div className="text-center p-3 bg-red-50 rounded-xl">
                    <input type="number" value={editForm.proteina_g} onChange={e => setEditForm(f => ({ ...f, proteina_g: Number(e.target.value) }))} className="w-full text-center text-2xl font-bold text-red-600 bg-transparent border-b border-red-300 focus:outline-none" />
                    <div className="text-xs text-red-500 mt-1">Proteína (g)</div>
                  </div>
                  <div className="text-center p-3 bg-blue-50 rounded-xl">
                    <input type="number" value={editForm.carboidratos_g} onChange={e => setEditForm(f => ({ ...f, carboidratos_g: Number(e.target.value) }))} className="w-full text-center text-2xl font-bold text-blue-600 bg-transparent border-b border-blue-300 focus:outline-none" />
                    <div className="text-xs text-blue-500 mt-1">Carbs (g)</div>
                  </div>
                  <div className="text-center p-3 bg-yellow-50 rounded-xl">
                    <input type="number" value={editForm.gorduras_g} onChange={e => setEditForm(f => ({ ...f, gorduras_g: Number(e.target.value) }))} className="w-full text-center text-2xl font-bold text-yellow-600 bg-transparent border-b border-yellow-300 focus:outline-none" />
                    <div className="text-xs text-yellow-500 mt-1">Gorduras (g)</div>
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-3 bg-orange-50 rounded-xl">
                    <div className="text-2xl font-bold text-orange-600">{plano.meta_calorica}</div>
                    <div className="text-xs text-orange-500">kcal/dia</div>
                  </div>
                  <div className="text-center p-3 bg-red-50 rounded-xl">
                    <div className="text-2xl font-bold text-red-600">{plano.proteina_g}g</div>
                    <div className="text-xs text-red-500">Proteína</div>
                  </div>
                  <div className="text-center p-3 bg-blue-50 rounded-xl">
                    <div className="text-2xl font-bold text-blue-600">{plano.carboidratos_g}g</div>
                    <div className="text-xs text-blue-500">Carboidratos</div>
                  </div>
                  <div className="text-center p-3 bg-yellow-50 rounded-xl">
                    <div className="text-2xl font-bold text-yellow-600">{plano.gorduras_g}g</div>
                    <div className="text-xs text-yellow-500">Gorduras</div>
                  </div>
                </div>
              )}

              {/* Plan details */}
              <div className="text-sm text-slate-600 space-y-2">
                {editing ? (
                  <div>
                    <strong>Objetivo:</strong>
                    <input type="text" value={editForm.objetivo} onChange={e => setEditForm(f => ({ ...f, objetivo: e.target.value }))} className="ml-2 border-b border-slate-300 focus:outline-none focus:border-ocean-500 bg-transparent w-2/3" />
                  </div>
                ) : (
                  <>
                    <p><strong>Objetivo:</strong> {plano.objetivo || "Não definido"}</p>
                    <p><strong>Início:</strong> {new Date(plano.data_inicio).toLocaleDateString("pt-BR")}</p>
                    {plano.data_fim && <p><strong>Fim:</strong> {new Date(plano.data_fim).toLocaleDateString("pt-BR")}</p>}
                    {plano.observacoes && <p><strong>Observações:</strong> {plano.observacoes}</p>}
                    <p className="text-xs text-slate-400 mt-2">Criado por: {plano.created_by} em {new Date(plano.created_at).toLocaleDateString("pt-BR")}</p>
                  </>
                )}
              </div>
            </div>

            {/* Meal Distribution */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
              <h3 className="font-semibold text-slate-800 mb-4">Distribuição de Refeições</h3>
              <div className="space-y-4">
                {(plano.refeicoes_detalhadas || refeicoesPadrao.map(r => ({ ...r, cal: Math.round(plano.meta_calorica * r.pct) }))).map((ref: any, i: number) => (
                  <div key={i} className="flex items-start gap-4 p-3 rounded-xl hover:bg-slate-50 transition-colors">
                    <div className="text-center min-w-[60px]">
                      <div className="text-sm font-mono text-slate-500">{ref.horario}</div>
                      <div className="text-xs text-ocean-600 font-semibold">{ref.cal || "—"} kcal</div>
                    </div>
                    <div>
                      <div className="font-medium text-slate-700">{ref.nome}</div>
                      <div className="text-sm text-slate-500">{ref.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* History of Plans */}
            {planos.length > 1 && (
              <div className="bg-white rounded-2xl border border-slate-200 p-6">
                <h3 className="font-semibold text-slate-800 mb-4">Histórico de Planos</h3>
                <div className="space-y-3">
                  {planos.map((p) => (
                    <div key={p.id} className={`flex items-center justify-between p-3 rounded-xl border ${p.id === plano.id ? "border-ocean-300 bg-ocean-50" : "border-slate-100 hover:bg-slate-50"} transition-colors`}>
                      <div className="flex items-center gap-3">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${p.ativo ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-500"}`}>
                          {p.ativo ? "Ativo" : "Inativo"}
                        </span>
                        <div>
                          <div className="text-sm font-medium text-slate-700">{p.meta_calorica} kcal — {p.objetivo || "Sem objetivo"}</div>
                          <div className="text-xs text-slate-400">Início: {new Date(p.data_inicio).toLocaleDateString("pt-BR")}</div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        {p.id !== plano.id && (
                          <button onClick={() => setPlano(p)} className="text-xs text-ocean-600 hover:underline">
                            Ver
                          </button>
                        )}
                        <button onClick={() => setShowConfirmDelete(p.id)} className="text-xs text-red-500 hover:underline">
                          Excluir
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {/* Delete Confirmation Modal */}
        {showConfirmDelete && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowConfirmDelete(null)}>
            <div className="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6" onClick={e => e.stopPropagation()}>
              <h3 className="font-semibold text-slate-800 mb-2">Confirmar exclusão</h3>
              <p className="text-sm text-slate-500 mb-6">Tem certeza que deseja excluir este plano nutricional? Esta ação não pode ser desfeita.</p>
              <div className="flex gap-3 justify-end">
                <button onClick={() => setShowConfirmDelete(null)} className="px-4 py-2 text-sm text-slate-500 hover:bg-slate-100 rounded-lg transition-colors">
                  Cancelar
                </button>
                <button onClick={() => deletePlano(showConfirmDelete)} className="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-500 transition-colors">
                  Excluir
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
