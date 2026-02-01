"use client";
import { useState, useRef, useEffect } from "react";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const {
    colaboradorId, messages, isLoading, conversaId,
    addMessage, updateLastAssistantMessage, setIsLoading, setConversaId,
  } = useAppStore();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isLoading || !colaboradorId) return;

    setInput("");
    addMessage({ role: "user", content: text, timestamp: new Date().toISOString() });
    setIsLoading(true);

    try {
      // Add empty assistant message for streaming
      addMessage({ role: "assistant", content: "", timestamp: new Date().toISOString() });
      let fullContent = "";

      for await (const chunk of api.enviarMensagemStream(colaboradorId, text, conversaId || undefined)) {
        if (chunk.type === "text") {
          fullContent += chunk.content;
          updateLastAssistantMessage(fullContent);
        } else if (chunk.type === "done" && chunk.conversa_id) {
          setConversaId(chunk.conversa_id);
        } else if (chunk.type === "error") {
          updateLastAssistantMessage(chunk.content || "Erro no servidor. Tente novamente.");
          setIsLoading(false);
          return;
        }
      }

      // If streaming didn't work, fall back to regular
      if (!fullContent) {
        const response = await api.enviarMensagem(colaboradorId, text, conversaId || undefined);
        updateLastAssistantMessage(response.resposta);
        setConversaId(response.conversa_id);
      }
    } catch (error) {
      updateLastAssistantMessage("Desculpe, ocorreu um erro. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 dark:bg-slate-900">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">🥗</div>
            <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-2">
              Ola! Sou o NutriOffshore
            </h3>
            <p className="text-slate-500 dark:text-slate-400 max-w-md mx-auto">
              Seu nutricionista virtual para a plataforma. Me conte seu objetivo
              ou pergunte sobre alimentacao!
            </p>
            <div className="flex flex-wrap gap-2 justify-center mt-6">
              {[
                "Quero perder peso neste embarque",
                "O que devo comer hoje?",
                "Sou diabetico, o que muda?",
                "Monte meu plano nutricional",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => { setInput(suggestion); inputRef.current?.focus(); }}
                  className="px-3 py-2 bg-ocean-50 dark:bg-ocean-900/30 text-ocean-700 dark:text-ocean-300 rounded-lg text-sm hover:bg-ocean-100 dark:hover:bg-ocean-900/50 transition-colors border border-ocean-200 dark:border-ocean-800"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {isLoading && messages[messages.length - 1]?.content === "" && (
          <div className="flex gap-1 px-4 py-3">
            <div className="w-2 h-2 bg-ocean-400 rounded-full typing-dot" />
            <div className="w-2 h-2 bg-ocean-400 rounded-full typing-dot" />
            <div className="w-2 h-2 bg-ocean-400 rounded-full typing-dot" />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={colaboradorId ? "Digite sua mensagem..." : "Selecione um colaborador primeiro"}
            disabled={!colaboradorId || isLoading}
            rows={1}
            className="flex-1 resize-none rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-100 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent disabled:bg-slate-100 dark:disabled:bg-slate-800 disabled:cursor-not-allowed placeholder:text-slate-400 dark:placeholder:text-slate-500"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading || !colaboradorId}
            className="px-6 py-3 bg-ocean-600 text-white rounded-xl font-medium hover:bg-ocean-500 transition-colors disabled:bg-slate-300 dark:disabled:bg-slate-600 disabled:cursor-not-allowed"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>
  );
}
