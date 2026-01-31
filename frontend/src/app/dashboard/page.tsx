"use client";
import { useState, useEffect } from "react";
import Header from "@/components/Header";
import MacroTracker from "@/components/MacroTracker";
import WeightChart from "@/components/WeightChart";

export default function DashboardPage() {
  // Demo data — in production, fetch from API
  const demoWeight = [
    { data: "2026-01-01", peso_kg: 88.5 },
    { data: "2026-01-07", peso_kg: 87.8 },
    { data: "2026-01-14", peso_kg: 87.2 },
    { data: "2026-01-21", peso_kg: 86.5 },
    { data: "2026-01-28", peso_kg: 86.0 },
  ];

  const demoMacros = {
    proteina: { atual: 120, meta: 160 },
    carboidratos: { atual: 180, meta: 250 },
    gorduras: { atual: 55, meta: 75 },
    calorias: { atual: 1680, meta: 2100 },
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">Dashboard Nutricional</h2>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Peso Atual", value: "86.0 kg", change: "-2.5 kg", positive: true },
            { label: "IMC", value: "26.3", change: "Sobrepeso", positive: false },
            { label: "Aderencia", value: "78%", change: "+5%", positive: true },
            { label: "Dias Embarcado", value: "12/14", change: "2 restantes", positive: true },
          ].map((stat, i) => (
            <div key={i} className="bg-white rounded-2xl border border-slate-200 p-4">
              <div className="text-sm text-slate-500 mb-1">{stat.label}</div>
              <div className="text-2xl font-bold text-slate-800">{stat.value}</div>
              <div className={`text-xs mt-1 ${stat.positive ? "text-nutri-green" : "text-nutri-yellow"}`}>
                {stat.change}
              </div>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid md:grid-cols-2 gap-6">
          <WeightChart data={demoWeight} />
          <MacroTracker {...demoMacros} />
        </div>

        {/* Recent meals */}
        <div className="mt-8 bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-semibold text-slate-800 mb-4">Refeicoes Recentes</h3>
          <div className="space-y-3">
            {[
              { refeicao: "Cafe da manha", hora: "06:15", cal: 480, aderencia: 90 },
              { refeicao: "Almoco", hora: "12:00", cal: 650, aderencia: 75 },
              { refeicao: "Lanche", hora: "15:30", cal: 180, aderencia: 100 },
              { refeicao: "Jantar", hora: "19:00", cal: 520, aderencia: 80 },
            ].map((r, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
                <div>
                  <span className="font-medium text-slate-700">{r.refeicao}</span>
                  <span className="text-sm text-slate-400 ml-2">{r.hora}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-slate-600">{r.cal} kcal</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    r.aderencia >= 80 ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"
                  }`}>
                    {r.aderencia}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
