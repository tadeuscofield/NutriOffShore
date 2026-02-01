import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="text-center p-8 bg-white rounded-2xl border border-slate-200 max-w-md">
        <div className="text-6xl mb-4 text-slate-300 font-bold">404</div>
        <h2 className="text-lg font-semibold text-slate-800 mb-2">
          Pagina nao encontrada
        </h2>
        <p className="text-sm text-slate-500 mb-6">
          A pagina que voce procura nao existe ou foi movida.
        </p>
        <Link
          href="/"
          className="inline-block px-6 py-2 bg-ocean-600 text-white rounded-xl hover:bg-ocean-500 transition-colors"
        >
          Voltar ao inicio
        </Link>
      </div>
    </div>
  );
}
