"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface WeightChartProps {
  data: { data: string; peso_kg: number }[];
}

export default function WeightChart({ data }: WeightChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-6">
        <h3 className="font-semibold text-slate-800 mb-4">Evolucao de Peso</h3>
        <p className="text-slate-400 text-sm text-center py-8">Sem dados de peso registrados</p>
      </div>
    );
  }

  const formatted = data.map((d) => ({
    data: new Date(d.data).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }),
    peso: d.peso_kg,
  }));

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <h3 className="font-semibold text-slate-800 mb-4">Evolucao de Peso</h3>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="data" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis domain={["dataMin - 2", "dataMax + 2"]} tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <Tooltip
            contentStyle={{
              borderRadius: "12px",
              border: "1px solid #e2e8f0",
              boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)",
            }}
          />
          <Line
            type="monotone"
            dataKey="peso"
            stroke="#0ea5e9"
            strokeWidth={2.5}
            dot={{ fill: "#0ea5e9", r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
