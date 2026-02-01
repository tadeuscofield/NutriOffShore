"use client";
import { useState, useEffect } from "react";
import Header from "@/components/Header";
import ChatWindow from "@/components/ChatWindow";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";
import type { Colaborador } from "@/lib/types";

export default function ChatPage() {
  const { colaboradorId, setColaborador, clearChat } = useAppStore();
  const [colaboradores, setColaboradores] = useState<Colaborador[]>([]);
  const [showSelector, setShowSelector] = useState(!colaboradorId);

  useEffect(() => {
    api.listarColaboradores().then(setColaboradores).catch(() => {});
  }, []);

  // Escape key handler for selector modal
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape" && showSelector && colaboradorId) {
        setShowSelector(false);
      }
    };
    document.addEventListener("keydown", handleEsc);
    return () => document.removeEventListener("keydown", handleEsc);
  }, [showSelector, colaboradorId]);

  const selectColaborador = (c: Colaborador) => {
    setColaborador(c);
    clearChat();
    setShowSelector(false);
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      <Header />

      {/* Colaborador selector bar */}
      <div className="bg-ocean-50 dark:bg-slate-800 border-b border-ocean-100 dark:border-slate-700 px-4 py-2 flex items-center gap-3">
        <span className="text-sm text-ocean-700 dark:text-ocean-300 font-medium">Colaborador:</span>
        {colaboradorId ? (
          <button
            onClick={() => setShowSelector(true)}
            className="text-sm text-ocean-600 dark:text-ocean-400 bg-white dark:bg-slate-700 px-3 py-1 rounded-lg border border-ocean-200 dark:border-slate-600 hover:bg-ocean-50 dark:hover:bg-slate-600"
          >
            {colaboradores.find(c => c.id === colaboradorId)?.nome || "Selecionar"} &#9662;
          </button>
        ) : (
          <button
            onClick={() => setShowSelector(true)}
            className="text-sm text-ocean-500 dark:text-ocean-400 bg-white dark:bg-slate-700 px-3 py-1 rounded-lg border border-dashed border-ocean-300 dark:border-slate-600 hover:bg-ocean-50 dark:hover:bg-slate-600"
          >
            Selecionar colaborador
          </button>
        )}
      </div>

      {/* Selector modal */}
      {showSelector && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          role="dialog"
          aria-modal="true"
          onClick={() => colaboradorId && setShowSelector(false)}
        >
          <div
            className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-md w-full max-h-[70vh] overflow-hidden"
            onClick={e => e.stopPropagation()}
          >
            <div className="p-4 border-b border-slate-200 dark:border-slate-700">
              <h2 className="font-semibold text-slate-800 dark:text-slate-100">Selecionar Colaborador</h2>
              <p className="text-sm text-slate-500 dark:text-slate-400">Escolha para iniciar a consulta</p>
            </div>
            <div className="overflow-y-auto max-h-[50vh] p-2">
              {colaboradores.length === 0 ? (
                <p className="text-center py-8 text-slate-400 dark:text-slate-500 text-sm">
                  Nenhum colaborador cadastrado. Cadastre na aba Perfil.
                </p>
              ) : (
                colaboradores.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => selectColaborador(c)}
                    className="w-full text-left p-3 rounded-xl hover:bg-ocean-50 dark:hover:bg-slate-700 transition-colors flex items-center gap-3"
                  >
                    <div className="w-10 h-10 bg-ocean-100 dark:bg-ocean-900/30 text-ocean-600 dark:text-ocean-400 rounded-full flex items-center justify-center font-semibold">
                      {c.nome.charAt(0)}
                    </div>
                    <div>
                      <div className="font-medium text-slate-800 dark:text-slate-100">{c.nome}</div>
                      <div className="text-xs text-slate-500 dark:text-slate-400">
                        {c.cargo || "Sem cargo"} &bull; {c.turno_atual} &bull; {c.regime_embarque}
                      </div>
                    </div>
                  </button>
                ))
              )}
            </div>
            <div className="p-3 border-t border-slate-200 dark:border-slate-700">
              {colaboradorId ? (
                <button
                  onClick={() => setShowSelector(false)}
                  className="w-full py-2 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                >
                  Cancelar
                </button>
              ) : (
                <p className="text-center text-xs text-slate-400 dark:text-slate-500">Selecione um colaborador para continuar</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Chat */}
      <div className="flex-1 overflow-hidden">
        <ChatWindow />
      </div>
    </div>
  );
}
