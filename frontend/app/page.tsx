import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 text-center">
      <h1 className="text-4xl font-bold">Nền tảng SEO nội bộ</h1>
      <p className="max-w-xl text-muted">
        Quản lý dự án SEO, tích hợp GSC/PSI/WordPress và theo dõi KPI trong một nơi duy nhất. Đăng nhập bằng tài khoản admin seed để khám phá demo.
      </p>
      <Link
        href="/dashboard"
        className="rounded-lg bg-brand-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-brand-600"
      >
        Đi tới bảng điều khiển
      </Link>
    </main>
  );
}
