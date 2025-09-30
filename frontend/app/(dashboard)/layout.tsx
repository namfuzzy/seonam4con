import Link from "next/link";
import { ReactNode } from "react";

import { ProjectSelector } from "@/components/project-selector";
import { QueryProvider } from "@/components/providers";

const navItems = [
  { href: "/dashboard", label: "Tổng quan" },
  { href: "/dashboard/du-an", label: "Dự án" },
  { href: "/dashboard/cai-dat", label: "Cài đặt" }
];

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <QueryProvider>
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <header className="border-b border-slate-800 bg-slate-900/70">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <div className="flex items-center gap-4">
              <span className="text-lg font-semibold text-brand-500">SEO nội bộ</span>
              <nav className="hidden gap-4 md:flex">
                {navItems.map((item) => (
                  <Link key={item.href} href={item.href} className="text-sm text-muted hover:text-white">
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>
            <ProjectSelector />
          </div>
        </header>
        <main className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-8">{children}</main>
      </div>
    </QueryProvider>
  );
}
