import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-ocean-900 via-ocean-800 to-ocean-950">
      {/* Header */}
      <header className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-ocean-400 rounded-xl flex items-center justify-center text-white font-bold text-lg">
            N
          </div>
          <h1 className="text-white text-xl font-bold">NutriOffshore AI</h1>
        </div>
        <nav className="flex gap-4">
          <Link href="/chat" className="text-ocean-200 hover:text-white transition-colors text-sm">
            Chat
          </Link>
          <Link href="/dashboard" className="text-ocean-200 hover:text-white transition-colors text-sm">
            Dashboard
          </Link>
          <Link href="/plano" className="text-ocean-200 hover:text-white transition-colors text-sm">
            Plano
          </Link>
          <Link href="/perfil" className="text-ocean-200 hover:text-white transition-colors text-sm">
            Perfil
          </Link>
        </nav>
      </header>

      {/* Hero */}
      <main className="max-w-5xl mx-auto px-6 pt-20 pb-32">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 bg-ocean-800/50 text-ocean-200 px-4 py-2 rounded-full text-sm mb-8 border border-ocean-700/50">
            <span className="w-2 h-2 bg-nutri-green rounded-full animate-pulse" />
            Agente IA Nutricionista Online
          </div>

          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Nutrição inteligente<br />
            para quem trabalha<br />
            <span className="text-ocean-400">no mar</span>
          </h2>

          <p className="text-ocean-300 text-lg md:text-xl max-w-2xl mx-auto mb-12">
            Planos nutricionais personalizados para colaboradores offshore.
            IA especializada em nutrição ocupacional, turnos e ambiente confinado.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/chat"
              className="px-8 py-4 bg-ocean-500 hover:bg-ocean-400 text-white rounded-xl font-semibold text-lg transition-colors shadow-lg shadow-ocean-500/25"
            >
              Iniciar Consulta
            </Link>
            <Link
              href="/dashboard"
              className="px-8 py-4 bg-ocean-800/50 hover:bg-ocean-700/50 text-ocean-100 rounded-xl font-semibold text-lg transition-colors border border-ocean-700/50"
            >
              Ver Dashboard
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mt-24">
          {[
            {
              icon: "🧮",
              title: "Cálculos Precisos",
              desc: "TMB, GET e macros calculados com fórmulas científicas adaptadas para offshore"
            },
            {
              icon: "🍽️",
              title: "Cardápio Inteligente",
              desc: "Sugestões baseadas no cardápio real do refeitório da plataforma"
            },
            {
              icon: "📊",
              title: "Acompanhamento",
              desc: "Evolução de peso, aderência e indicadores de saúde em tempo real"
            },
            {
              icon: "🌙",
              title: "Turno Noturno",
              desc: "Ajustes específicos para cronobiologia e trabalho noturno"
            },
            {
              icon: "⚠️",
              title: "Alertas Médicos",
              desc: "Identificação automática de sinais de alerta e encaminhamento"
            },
            {
              icon: "💧",
              title: "Hidratação",
              desc: "Protocolo personalizado para ambiente climatizado offshore"
            },
          ].map((feature, i) => (
            <div
              key={i}
              className="bg-ocean-800/30 border border-ocean-700/30 rounded-2xl p-6 hover:bg-ocean-800/50 transition-colors"
            >
              <span className="text-3xl mb-4 block">{feature.icon}</span>
              <h3 className="text-white font-semibold text-lg mb-2">{feature.title}</h3>
              <p className="text-ocean-300 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-ocean-800 py-6 text-center text-ocean-400 text-sm">
        NutriOffshore AI &copy; {new Date().getFullYear()} &mdash; Nutrição ocupacional inteligente
      </footer>
    </div>
  );
}
