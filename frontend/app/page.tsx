import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 text-center">
      <div className="max-w-2xl space-y-4">
        <h1 className="text-4xl font-bold text-white md:text-5xl">SEO Nội Bộ</h1>
        <p className="text-lg text-slate-300">
          Nền tảng SEO nội bộ all-in-one giúp đội marketing theo dõi hiệu suất, tối ưu nội dung và tự động hoá quy trình trên WordPress.
        </p>
        <div className="flex justify-center gap-3">
          <Link href="/dashboard" className="rounded-lg bg-emerald-500 px-4 py-2 font-semibold text-slate-950 transition hover:bg-emerald-400">
            Vào bảng điều khiển demo
          </Link>
          <Link href="https://github.com" className="rounded-lg border border-slate-700 px-4 py-2 font-semibold text-slate-200 transition hover:border-slate-500">
            Tài liệu triển khai
          </Link>
        </div>
      </div>
    </main>
  );
}
