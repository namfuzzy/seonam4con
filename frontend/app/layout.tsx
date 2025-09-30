import "../styles/globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "SEO nội bộ",
  description: "Bảng điều khiển SEO nội bộ đa dự án"
};

export default function RootLayout({ children }: { children: ReactNode }) {
    return (
        <html lang="vi" className="dark">
            <body className="bg-slate-950 text-slate-100">
                {children}
            </body>
        </html>
    );
}
