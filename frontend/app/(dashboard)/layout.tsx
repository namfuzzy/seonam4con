import { ReactNode } from "react";
import Link from "next/link";

import { ProjectSelector } from "../../components/project-selector";

const navItems = [
  { href: "/dashboard", label: "Tổng quan" },
  { href: "/du-an", label: "Dự án" }
];

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 flex-col border-r border-slate-800 bg-slate-900/60 p-6 lg:flex">
        <div className="mb-6 space-y-1">
          <h2 className="text-xl font-semibold text-white">SEO Nội Bộ</h2>
          <p className="text-sm text-slate-400">Quản trị đa dự án & tích hợp</p>
        </div>
        <nav className="flex flex-1 flex-col gap-2">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-lg px-3 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="text-xs text-slate-500">Phiên bản MVP v1.0</div>
      </aside>
      <main className="lg:pl-64">
        <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <div className="text-sm text-slate-400">Dự án hiện tại</div>
              <ProjectSelector />
            </div>
            <div className="text-right text-sm text-slate-400">
              <div>admin@demo.local</div>
              <div className="text-xs">Owner</div>
            </div>
          </div>
        </header>
        <div className="space-y-6 p-6">{children}</div>
      </main>
    </div>
  );
}

