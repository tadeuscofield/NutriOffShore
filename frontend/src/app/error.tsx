"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="text-center p-8 bg-white rounded-2xl border border-slate-200 max-w-md">
        <div className="text-4xl mb-4">&#9888;&#65039;</div>
        <h2 className="text-lg font-semibold text-slate-800 mb-2">
          Algo deu errado
        </h2>
        <p className="text-sm text-slate-500 mb-6">
          {error.message || "Ocorreu um erro inesperado."}
        </p>
        <button
          onClick={reset}
          className="px-6 py-2 bg-ocean-600 text-white rounded-xl hover:bg-ocean-500 transition-colors"
        >
          Tentar novamente
        </button>
      </div>
    </div>
  );
}
