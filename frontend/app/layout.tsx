import "../styles/globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";

import { Providers } from "../components/providers";

export const metadata: Metadata = {
  title: "SEO Nội Bộ",
  description: "Nền tảng SEO nội bộ all-in-one"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
