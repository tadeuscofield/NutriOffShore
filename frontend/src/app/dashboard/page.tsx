"use client";
import { useState, useEffect, useCallback } from "react";
import Header from "@/components/Header";
import MacroTracker from "@/components/MacroTracker";
import WeightChart from "@/components/WeightChart";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";

interface Medicao {
  data_medicao: string;
  peso_kg: number | null;
  percentual_gordura: number | null;
  glicemia_jejum: number | null;
  colesterol_total: number | null;
  pressao_sistolica: number | null;
  pressao_diastolica: number | null;
}

interface Plano {
  id: string;
  meta_calorica: number;
  proteina_g: number;
  carboidratos_g: number;
  gorduras_g: number;
  objetivo: string | null;
  ativo: boolean;
  data_inicio: string;
}

interface Alerta {
  id: string;
  tipo: string;
  motivo: string;
  status: string;
  created_at: string;
}

interface ResumoRefeicao {
  data: string;
  total_calorias: number;
  total_proteina_g: number;
  total_carboidratos_g: number;
  total_gorduras_g: number;
  refeicoes_registradas: number;
  aderencia_media: number | null;
}

function calcularIMC(pesoKg: number, alturaCm: number | null): { imc: number; classificacao: string } | null {
  if (!alturaCm || alturaCm <= 0 || pesoKg <= 0) return null;
  const alturaM = alturaCm / 100;
  const imc = pesoKg / (alturaM * alturaM);
  let classificacao = "";
  if (imc < 18.5) classificacao = "Abaixo do peso";
  else if (imc < 25) classificacao = "Peso normal";
  else if (imc < 30) classificacao = "Sobrepeso";
  else if (imc < 35) classificacao = "Obesidade I";
  else if (imc < 40) classificacao = "Obesidade II";
  else classificacao = "Obesidade III";
  return { imc: Math.round(imc * 10) / 10, classificacao };
}

export default function DashboardPage() {
  const { colaboradorId, colaborador } = useAppStore();
  const [medicoes, setMedicoes] = useState<Medicao[]>([]);
  const [plano, setPlano] = useState<Plano | null>(null);
  const [alertas, setAlertas] = useState<Alerta[]>([]);
  const [resumoRefeicoes, setResumoRefeicoes] = useState<ResumoRefeicao[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    if (!colaboradorId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);

    const results = await Promise.allSettled([
      api.buscarColaborador(colaboradorId),
      api.planoAtivo(colaboradorId),
      api.listarRefeicoes(colaboradorId),
      api.listarAlertasColaborador(colaboradorId),
    ]);

    // Medicoes from full collaborator response
    if (results[0].status === "fulfilled") {
      const fullColaborador = results[0].value;
      setMedicoes(fullColaborador.medicoes || []);
    } else {
      // Fallback: try direct medicoes endpoint
      try {
        const m = await api.listarMedicoes(colaboradorId);
        setMedicoes(m || []);
      } catch {
        setMedicoes([]);
      }
    }

    // Plano ativo
    if (results[1].status === "fulfilled") {
      setPlano(results[1].value);
    } else {
      setPlano(null);
    }

    // Resumo refeicoes
    if (results[2].status === "fulfilled") {
      const data = results[2].value;
      setResumoRefeicoes(Array.isArray(data) ? data : (data as { dias?: ResumoRefeicao[] })?.dias || []);
    } else {
      setResumoRefeicoes([]);
    }

    // Alertas
    if (results[3].status === "fulfilled") {
      setAlertas(results[3].value || []);
    } else {
      // Fallback: try general alertas endpoint
      try {
        const a = await api.listarAlertas("aberto");
        setAlertas(a || []);
      } catch {
        setAlertas([]);
      }
    }

    setLoading(false);
  }, [colaboradorId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Derived data
  const sortedMedicoes = [...medicoes].sort(
    (a, b) => new Date(a.data_medicao).getTime() - new Date(b.data_medicao).getTime()
  );
  const latestMedicao = sortedMedicoes.length > 0 ? sortedMedicoes[sortedMedicoes.length - 1] : null;
  const firstMedicao = sortedMedicoes.length > 1 ? sortedMedicoes[0] : null;

  const pesoAtual = latestMedicao?.peso_kg;
  const pesoDiff = pesoAtual && firstMedicao?.peso_kg
    ? Math.round((pesoAtual - firstMedicao.peso_kg) * 10) / 10
    : null;

  const imcData = pesoAtual ? calcularIMC(pesoAtual, colaborador?.altura_cm ?? null) : null;

  const weightChartData = sortedMedicoes
    .filter((m) => m.peso_kg !== null)
    .map((m) => ({ data: m.data_medicao, peso_kg: m.peso_kg! }));

  // Macro tracker from today's meals (latest day in resumo)
  const latestResumo = resumoRefeicoes.length > 0 ? resumoRefeicoes[resumoRefeicoes.length - 1] : null;
  const macroData = {
    proteina: {
      atual: latestResumo?.total_proteina_g || 0,
      meta: plano?.proteina_g || 160,
    },
    carboidratos: {
      atual: latestResumo?.total_carboidratos_g || 0,
      meta: plano?.carboidratos_g || 250,
    },
    gorduras: {
      atual: latestResumo?.total_gorduras_g || 0,
      meta: plano?.gorduras_g || 75,
    },
    calorias: {
      atual: latestResumo?.total_calorias || 0,
      meta: plano?.meta_calorica || 2100,
    },
  };

  const aderenciaMedia = resumoRefeicoes.length > 0
    ? Math.round(
        resumoRefeicoes.reduce((acc: number, r: ResumoRefeicao) => acc + (r.aderencia_media || 0), 0) / resumoRefeicoes.length
      )
    : null;

  // No collaborator selected
  if (!colaboradorId) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
        <Header />
        <main className="max-w-6xl mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">Dashboard Nutricional</h2>
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-12 text-center">
            <div className="text-4xl mb-3">📊</div>
            <p className="text-slate-500 dark:text-slate-400">
              Selecione um colaborador na aba <strong>Chat</strong> para ver o dashboard nutricional.
            </p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Dashboard Nutricional</h2>
          {colaborador && (
            <span className="text-sm text-ocean-600 dark:text-ocean-400 bg-ocean-50 dark:bg-ocean-900/30 px-3 py-1 rounded-lg">
              {colaborador.nome}
            </span>
          )}
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg text-sm bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800">
            {error}
          </div>
        )}

        {loading ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4 animate-pulse">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3 mb-2" />
                  <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/2" />
                </div>
              ))}
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 h-[300px] animate-pulse" />
              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 h-[300px] animate-pulse" />
            </div>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4">
                <div className="text-sm text-slate-500 dark:text-slate-400 mb-1">Peso Atual</div>
                <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                  {pesoAtual ? `${pesoAtual} kg` : "---"}
                </div>
                {pesoDiff !== null && (
                  <div className={`text-xs mt-1 ${pesoDiff <= 0 ? "text-nutri-green" : "text-nutri-yellow"}`}>
                    {pesoDiff > 0 ? "+" : ""}{pesoDiff} kg
                  </div>
                )}
              </div>

              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4">
                <div className="text-sm text-slate-500 dark:text-slate-400 mb-1">IMC</div>
                <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                  {imcData ? imcData.imc : "---"}
                </div>
                <div className={`text-xs mt-1 ${imcData && imcData.imc < 25 ? "text-nutri-green" : "text-nutri-yellow"}`}>
                  {imcData ? imcData.classificacao : "Sem dados"}
                </div>
              </div>

              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4">
                <div className="text-sm text-slate-500 dark:text-slate-400 mb-1">Aderencia</div>
                <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                  {aderenciaMedia !== null ? `${aderenciaMedia}%` : "---"}
                </div>
                <div className={`text-xs mt-1 ${aderenciaMedia !== null && aderenciaMedia >= 70 ? "text-nutri-green" : "text-nutri-yellow"}`}>
                  {aderenciaMedia !== null ? "Semanal" : "Sem dados"}
                </div>
              </div>

              <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4">
                <div className="text-sm text-slate-500 dark:text-slate-400 mb-1">Meta Calorica</div>
                <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                  {plano ? `${plano.meta_calorica}` : "---"}
                </div>
                <div className="text-xs mt-1 text-ocean-600 dark:text-ocean-400">
                  {plano ? `kcal/dia - ${plano.objetivo || "Geral"}` : "Sem plano ativo"}
                </div>
              </div>
            </div>

            {/* Charts */}
            <div className="grid md:grid-cols-2 gap-6">
              <WeightChart data={weightChartData} />
              <MacroTracker {...macroData} />
            </div>

            {/* Alertas */}
            {alertas.length > 0 && (
              <div className="mt-8 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
                <h3 className="font-semibold text-slate-800 dark:text-slate-100 mb-4">Alertas Ativos</h3>
                <div className="space-y-3">
                  {alertas.slice(0, 5).map((alerta) => (
                    <div
                      key={alerta.id}
                      className="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-700 last:border-0"
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                            alerta.tipo === "urgente"
                              ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                              : alerta.tipo === "moderado"
                              ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300"
                              : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                          }`}
                        >
                          {alerta.tipo}
                        </span>
                        <span className="text-sm text-slate-700 dark:text-slate-300">{alerta.motivo}</span>
                      </div>
                      <span className="text-xs text-slate-400 dark:text-slate-500">
                        {new Date(alerta.created_at).toLocaleDateString("pt-BR")}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recent meals summary */}
            <div className="mt-8 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
              <h3 className="font-semibold text-slate-800 dark:text-slate-100 mb-4">Resumo Semanal de Refeicoes</h3>
              {resumoRefeicoes.length === 0 ? (
                <p className="text-sm text-slate-400 dark:text-slate-500 text-center py-4">
                  Nenhuma refeicao registrada recentemente.
                </p>
              ) : (
                <div className="space-y-3">
                  {resumoRefeicoes.slice(-7).map((r, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-700 last:border-0"
                    >
                      <div>
                        <span className="font-medium text-slate-700 dark:text-slate-300">
                          {new Date(r.data).toLocaleDateString("pt-BR", { weekday: "short", day: "2-digit", month: "2-digit" })}
                        </span>
                        <span className="text-sm text-slate-400 dark:text-slate-500 ml-2">
                          {r.refeicoes_registradas} refeicoes
                        </span>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="text-sm text-slate-600 dark:text-slate-400">{r.total_calorias} kcal</span>
                        {r.aderencia_media !== null && (
                          <span
                            className={`text-xs px-2 py-0.5 rounded-full ${
                              r.aderencia_media >= 80
                                ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
                                : "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300"
                            }`}
                          >
                            {Math.round(r.aderencia_media)}%
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
