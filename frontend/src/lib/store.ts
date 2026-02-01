import { create } from "zustand";
import type { ChatMessage, Colaborador } from "./types";

interface AppState {
  colaboradorId: string | null;
  colaborador: Colaborador | null;
  conversaId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  darkMode: boolean;

  setColaboradorId: (id: string) => void;
  setColaborador: (c: Colaborador) => void;
  setConversaId: (id: string | null) => void;
  addMessage: (msg: ChatMessage) => void;
  setMessages: (msgs: ChatMessage[]) => void;
  updateLastAssistantMessage: (content: string) => void;
  setIsLoading: (loading: boolean) => void;
  clearChat: () => void;
  toggleDarkMode: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  colaboradorId: null,
  colaborador: null,
  conversaId: null,
  messages: [],
  isLoading: false,
  darkMode: typeof window !== "undefined"
    ? localStorage.getItem("darkMode") === "true"
    : false,

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
  toggleDarkMode: () =>
    set((state) => {
      const newMode = !state.darkMode;
      if (typeof window !== "undefined") {
        localStorage.setItem("darkMode", String(newMode));
      }
      return { darkMode: newMode };
    }),
}));
