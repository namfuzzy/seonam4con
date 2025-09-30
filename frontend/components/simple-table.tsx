import { ReactNode } from "react";

interface Column<T> {
  key: keyof T;
  header: string;
  render?: (item: T) => ReactNode;
}

interface SimpleTableProps<T> {
  columns: Column<T>[];
  data: T[];
}

export function SimpleTable<T extends Record<string, any>>({ columns, data }: SimpleTableProps<T>) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800">
        <thead className="bg-slate-900/70">
          <tr>
            {columns.map((column) => (
              <th key={String(column.key)} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-400">
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {data.map((row, index) => (
            <tr key={index} className="bg-slate-950/40 hover:bg-slate-900/40">
              {columns.map((column) => (
                <td key={String(column.key)} className="px-4 py-3 text-sm text-slate-200">
                  {column.render ? column.render(row) : (row[column.key] as ReactNode)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
