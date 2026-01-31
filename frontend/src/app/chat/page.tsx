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

  const selectColaborador = (c: Colaborador) => {
    setColaborador(c);
    clearChat();
    setShowSelector(false);
  };

  return (
    <div className="flex flex-col h-screen">
      <Header />
      
      {/* Colaborador selector bar */}
      <div className="bg-ocean-50 border-b border-ocean-100 px-4 py-2 flex items-center gap-3">
        <span className="text-sm text-ocean-700 font-medium">Colaborador:</span>
        {colaboradorId ? (
          <button
            onClick={() => setShowSelector(true)}
            className="text-sm text-ocean-600 bg-white px-3 py-1 rounded-lg border border-ocean-200 hover:bg-ocean-50"
          >
            {colaboradores.find(c => c.id === colaboradorId)?.nome || "Selecionar"} &#9662;
          </button>
        ) : (
          <button
            onClick={() => setShowSelector(true)}
            className="text-sm text-ocean-500 bg-white px-3 py-1 rounded-lg border border-dashed border-ocean-300 hover:bg-ocean-50"
          >
            Selecionar colaborador
          </button>
        )}
      </div>

      {/* Selector modal */}
      {showSelector && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => colaboradorId && setShowSelector(false)}
        >
          <div
            className="bg-white rounded-2xl shadow-xl max-w-md w-full max-h-[70vh] overflow-hidden"
            onClick={e => e.stopPropagation()}
          >
            <div className="p-4 border-b border-slate-200">
              <h2 className="font-semibold text-slate-800">Selecionar Colaborador</h2>
              <p className="text-sm text-slate-500">Escolha para iniciar a consulta</p>
            </div>
            <div className="overflow-y-auto max-h-[50vh] p-2">
              {colaboradores.length === 0 ? (
                <p className="text-center py-8 text-slate-400 text-sm">
                  Nenhum colaborador cadastrado. Cadastre na aba Perfil.
                </p>
              ) : (
                colaboradores.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => selectColaborador(c)}
                    className="w-full text-left p-3 rounded-xl hover:bg-ocean-50 transition-colors flex items-center gap-3"
                  >
                    <div className="w-10 h-10 bg-ocean-100 text-ocean-600 rounded-full flex items-center justify-center font-semibold">
                      {c.nome.charAt(0)}
                    </div>
                    <div>
                      <div className="font-medium text-slate-800">{c.nome}</div>
                      <div className="text-xs text-slate-500">
                        {c.cargo || "Sem cargo"} &bull; {c.turno_atual} &bull; {c.regime_embarque}
                      </div>
                    </div>
                  </button>
                ))
              )}
            </div>
            <div className="p-3 border-t border-slate-200">
              {colaboradorId ? (
                <button
                  onClick={() => setShowSelector(false)}
                  className="w-full py-2 text-sm text-slate-500 hover:text-slate-700"
                >
                  Cancelar
                </button>
              ) : (
                <p className="text-center text-xs text-slate-400">Selecione um colaborador para continuar</p>
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
