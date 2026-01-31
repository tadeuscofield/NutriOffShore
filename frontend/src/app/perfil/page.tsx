"use client";
import { useState } from "react";
import Header from "@/components/Header";
import { api } from "@/lib/api";

interface ProfileFormData {
  nome: string;
  matricula: string;
  data_nascimento: string;
  sexo: string;
  altura_cm: string;
  cargo: string;
  nivel_atividade: string;
  turno_atual: string;
  regime_embarque: string;
  meta_principal: string;
}

export default function PerfilPage() {
  const [formData, setFormData] = useState<ProfileFormData>({
    nome: "", matricula: "", data_nascimento: "", sexo: "M",
    altura_cm: "", cargo: "", nivel_atividade: "moderado",
    turno_atual: "diurno", regime_embarque: "14x14", meta_principal: "saude_geral",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  const inputClasses = "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:ring-2 focus:ring-ocean-500 focus:border-transparent";
  const labelClasses = "block text-sm font-medium text-slate-700 mb-1";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    try {
      await api.criarColaborador({ ...formData, altura_cm: Number(formData.altura_cm) || null });
      setMessage({ text: "Colaborador cadastrado com sucesso!", type: "success" });
      setFormData({
        nome: "", matricula: "", data_nascimento: "", sexo: "M",
        altura_cm: "", cargo: "", nivel_atividade: "moderado",
        turno_atual: "diurno", regime_embarque: "14x14", meta_principal: "saude_geral",
      });
    } catch (err) {
      setMessage({ text: err instanceof Error ? err.message : "Erro de conexao com o servidor", type: "error" });
    } finally {
      setLoading(false);
    }
  };

  const updateField = (field: keyof ProfileFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main className="max-w-2xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">Cadastro / Perfil</h2>

        {message && (
          <div className={`mb-4 p-3 rounded-lg text-sm ${message.type === "success" ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div><label className={labelClasses}>Nome</label><input type="text" value={formData.nome} onChange={e => updateField("nome", e.target.value)} className={inputClasses} required /></div>
            <div><label className={labelClasses}>Matricula</label><input type="text" value={formData.matricula} onChange={e => updateField("matricula", e.target.value)} className={inputClasses} required /></div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div><label className={labelClasses}>Nascimento</label><input type="date" value={formData.data_nascimento} onChange={e => updateField("data_nascimento", e.target.value)} className={inputClasses} required /></div>
            <div><label className={labelClasses}>Sexo</label><select value={formData.sexo} onChange={e => updateField("sexo", e.target.value)} className={inputClasses}><option value="M">Masculino</option><option value="F">Feminino</option></select></div>
            <div><label className={labelClasses}>Altura (cm)</label><input type="number" value={formData.altura_cm} onChange={e => updateField("altura_cm", e.target.value)} className={inputClasses} /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className={labelClasses}>Cargo</label><input type="text" value={formData.cargo} onChange={e => updateField("cargo", e.target.value)} className={inputClasses} /></div>
            <div><label className={labelClasses}>Nivel Atividade</label><select value={formData.nivel_atividade} onChange={e => updateField("nivel_atividade", e.target.value)} className={inputClasses}><option value="sedentario">Sedentario</option><option value="leve">Leve</option><option value="moderado">Moderado</option><option value="intenso">Intenso</option></select></div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div><label className={labelClasses}>Turno</label><select value={formData.turno_atual} onChange={e => updateField("turno_atual", e.target.value)} className={inputClasses}><option value="diurno">Diurno</option><option value="noturno">Noturno</option></select></div>
            <div><label className={labelClasses}>Regime</label><select value={formData.regime_embarque} onChange={e => updateField("regime_embarque", e.target.value)} className={inputClasses}><option value="14x14">14x14</option><option value="21x21">21x21</option><option value="28x28">28x28</option></select></div>
            <div><label className={labelClasses}>Objetivo</label><select value={formData.meta_principal} onChange={e => updateField("meta_principal", e.target.value)} className={inputClasses}><option value="perda_peso">Perda de peso</option><option value="ganho_massa">Ganho de massa</option><option value="manutencao">Manutencao</option><option value="performance">Performance</option><option value="saude_geral">Saude geral</option></select></div>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-ocean-600 text-white rounded-xl font-semibold hover:bg-ocean-500 transition-colors disabled:bg-slate-300 disabled:cursor-not-allowed"
          >
            {loading ? "Cadastrando..." : "Cadastrar Colaborador"}
          </button>
        </form>
      </main>
    </div>
  );
}
