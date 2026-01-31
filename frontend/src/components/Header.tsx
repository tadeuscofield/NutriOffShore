"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Header() {
  const pathname = usePathname();

  const links = [
    { href: "/chat", label: "Chat" },
    { href: "/dashboard", label: "Dashboard" },
    { href: "/plano", label: "Plano" },
    { href: "/perfil", label: "Perfil" },
  ];

  return (
    <header className="bg-ocean-900 border-b border-ocean-800 px-4 py-3 flex items-center justify-between sticky top-0 z-50">
      <Link href="/" className="flex items-center gap-2">
        <div className="w-8 h-8 bg-ocean-500 rounded-lg flex items-center justify-center text-white font-bold text-sm">
          N
        </div>
        <span className="text-white font-semibold hidden sm:inline">NutriOffshore</span>
      </Link>
      <nav className="flex gap-1">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              pathname === link.href
                ? "bg-ocean-700 text-white"
                : "text-ocean-300 hover:text-white hover:bg-ocean-800"
            }`}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
