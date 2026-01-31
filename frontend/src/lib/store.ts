import { create } from "zustand";
import type { ChatMessage, Colaborador } from "./types";

interface AppState {
  colaboradorId: string | null;
  colaborador: Colaborador | null;
  conversaId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  
  setColaboradorId: (id: string) => void;
  setColaborador: (c: Colaborador) => void;
  setConversaId: (id: string | null) => void;
  addMessage: (msg: ChatMessage) => void;
  setMessages: (msgs: ChatMessage[]) => void;
  updateLastAssistantMessage: (content: string) => void;
  setIsLoading: (loading: boolean) => void;
  clearChat: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  colaboradorId: null,
  colaborador: null,
  conversaId: null,
  messages: [],
  isLoading: false,

  setColaboradorId: (id) => set({ colaboradorId: id }),
  setColaborador: (c) => set({ colaborador: c, colaboradorId: c.id }),
  setConversaId: (id) => set({ conversaId: id }),
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  setMessages: (msgs) => set({ messages: msgs }),
  updateLastAssistantMessage: (content) =>
    set((state) => {
      const msgs = [...state.messages];
      const lastIdx = msgs.length - 1;
      if (lastIdx >= 0 && msgs[lastIdx].role === "assistant") {
        msgs[lastIdx] = { ...msgs[lastIdx], content };
      }
      return { messages: msgs };
    }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  clearChat: () => set({ messages: [], conversaId: null }),
}));
