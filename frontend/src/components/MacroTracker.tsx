"use client";

interface MacroTrackerProps {
  proteina: { atual: number; meta: number };
  carboidratos: { atual: number; meta: number };
  gorduras: { atual: number; meta: number };
  calorias: { atual: number; meta: number };
}

export default function MacroTracker({ proteina, carboidratos, gorduras, calorias }: MacroTrackerProps) {
  const macros = [
    { label: "Calorias", atual: calorias.atual, meta: calorias.meta, unit: "kcal", color: "bg-orange-500" },
    { label: "Proteína", atual: proteina.atual, meta: proteina.meta, unit: "g", color: "bg-red-500" },
    { label: "Carbs", atual: carboidratos.atual, meta: carboidratos.meta, unit: "g", color: "bg-blue-500" },
    { label: "Gorduras", atual: gorduras.atual, meta: gorduras.meta, unit: "g", color: "bg-yellow-500" },
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6">
      <h3 className="font-semibold text-slate-800 mb-4">Macros do Dia</h3>
      <div className="space-y-4">
        {macros.map((macro) => {
          const pct = Math.min((macro.atual / macro.meta) * 100, 100);
          return (
            <div key={macro.label}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-600">{macro.label}</span>
                <span className="text-slate-800 font-medium">
                  {macro.atual} / {macro.meta} {macro.unit}
                </span>
              </div>
              <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${macro.color} rounded-full transition-all duration-500`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
