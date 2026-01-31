"use client";
import Header from "@/components/Header";

export default function PlanoPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">Plano Nutricional</h2>
        
        {/* Active Plan */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-800">Plano Ativo</h3>
            <span className="text-xs bg-nutri-green/10 text-nutri-green px-3 py-1 rounded-full font-medium">
              Ativo
            </span>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-3 bg-orange-50 rounded-xl">
              <div className="text-2xl font-bold text-orange-600">2100</div>
              <div className="text-xs text-orange-500">kcal/dia</div>
            </div>
            <div className="text-center p-3 bg-red-50 rounded-xl">
              <div className="text-2xl font-bold text-red-600">160g</div>
              <div className="text-xs text-red-500">Proteina</div>
            </div>
            <div className="text-center p-3 bg-blue-50 rounded-xl">
              <div className="text-2xl font-bold text-blue-600">250g</div>
              <div className="text-xs text-blue-500">Carbs</div>
            </div>
            <div className="text-center p-3 bg-yellow-50 rounded-xl">
              <div className="text-2xl font-bold text-yellow-600">75g</div>
              <div className="text-xs text-yellow-500">Gorduras</div>
            </div>
          </div>

          <div className="text-sm text-slate-600 space-y-2">
            <p><strong>Objetivo:</strong> Perda de peso com preservacao de massa muscular</p>
            <p><strong>Deficit:</strong> -400 kcal (GET: 2500 kcal)</p>
            <p><strong>Hidratacao:</strong> 3000 ml/dia</p>
            <p><strong>Fibra:</strong> 30g/dia</p>
          </div>
        </div>

        {/* Meal plan */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-semibold text-slate-800 mb-4">Distribuicao de Refeicoes</h3>
          <div className="space-y-4">
            {[
              { nome: "Cafe da manha", horario: "06:00", cal: 480, desc: "Proteina + carboidrato integral + fruta" },
              { nome: "Lanche manha", horario: "09:30", cal: 180, desc: "Fruta com castanhas ou iogurte" },
              { nome: "Almoco", horario: "12:00", cal: 650, desc: "Proteina magra + arroz/batata + salada abundante" },
              { nome: "Lanche tarde", horario: "15:30", cal: 180, desc: "Iogurte natural ou fruta + proteina" },
              { nome: "Jantar", horario: "19:00", cal: 520, desc: "Proteina + legumes + carb moderado" },
              { nome: "Ceia", horario: "21:00", cal: 90, desc: "Cha + 1 torrada integral (se necessario)" },
            ].map((ref, i) => (
              <div key={i} className="flex items-start gap-4 p-3 rounded-xl hover:bg-slate-50 transition-colors">
                <div className="text-center min-w-[60px]">
                  <div className="text-sm font-mono text-slate-500">{ref.horario}</div>
                  <div className="text-xs text-ocean-600 font-semibold">{ref.cal} kcal</div>
                </div>
                <div>
                  <div className="font-medium text-slate-700">{ref.nome}</div>
                  <div className="text-sm text-slate-500">{ref.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
