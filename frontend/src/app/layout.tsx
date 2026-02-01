import type { Metadata, Viewport } from "next";
import "./globals.css";
import DarkModeProvider from "@/components/DarkModeProvider";

export const metadata: Metadata = {
  title: "NutriOffshore AI",
  description: "Nutricionista Virtual para Plataformas Offshore de Óleo e Gás",
  manifest: "/manifest.json",
  icons: {
    icon: "/icon.svg",
    apple: "/icon.svg",
  },
};

export const viewport: Viewport = {
  themeColor: "#0ea5e9",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-50 dark:bg-slate-900 transition-colors">
        <DarkModeProvider>
          {children}
        </DarkModeProvider>
      </body>
    </html>
  );
}
