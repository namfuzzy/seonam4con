"use client";

import { FormEvent, useState } from "react";

interface Field {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
}

interface IntegrationCardProps {
  title: string;
  description: string;
  fields: Field[];
  onSubmit?: (values: Record<string, string>) => Promise<void> | void;
  onToggle?: (enabled: boolean) => Promise<void> | void;
  defaultEnabled?: boolean;
}

export function IntegrationCard({ title, description, fields, onSubmit, onToggle, defaultEnabled = false }: IntegrationCardProps) {
  const [enabled, setEnabled] = useState(defaultEnabled);
  const [values, setValues] = useState<Record<string, string>>({});
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (onSubmit) {
      await onSubmit(values);
      setMessage("Đã lưu & mã hoá thông tin");
    }
  };

  return (
    <section className="space-y-3 rounded-xl border border-slate-800 bg-slate-900/60 p-5">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <p className="text-sm text-slate-400">{description}</p>
        </div>
        <label className="flex cursor-pointer items-center gap-2 text-sm text-slate-300">
          <input
            type="checkbox"
            checked={enabled}
            onChange={(event) => {
              setEnabled(event.target.checked);
              onToggle?.(event.target.checked);
            }}
            className="h-4 w-4 accent-emerald-500"
          />
          Bật
        </label>
      </div>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
        {fields.map((field) => (
          <label key={field.name} className="space-y-2 text-sm">
            <span className="text-slate-300">{field.label}</span>
            <input
              type={field.type ?? "password"}
              placeholder={field.placeholder}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              onChange={(event) => setValues((prev) => ({ ...prev, [field.name]: event.target.value }))}
            />
          </label>
        ))}
        <button type="submit" className="mt-6 w-full rounded-lg bg-emerald-500 px-4 py-2 font-semibold text-slate-950 md:col-span-2">
          Lưu & mã hoá
        </button>
      </form>
      {message && <p className="text-xs text-emerald-300">{message}</p>}
    </section>
  );
}
