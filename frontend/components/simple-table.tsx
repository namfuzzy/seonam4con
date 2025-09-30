interface Column<T> {
  header: string;
  accessor: (item: T) => string;
}

interface SimpleTableProps<T> {
  data: T[];
  columns: Column<T>[];
  emptyText: string;
}

export function SimpleTable<T>({ data, columns, emptyText }: SimpleTableProps<T>) {
  if (data.length === 0) {
    return <p className="text-sm text-muted">{emptyText}</p>;
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800">
        <thead className="bg-slate-900/60">
          <tr>
            {columns.map((column) => (
              <th key={column.header} className="px-4 py-3 text-left text-xs font-medium uppercase text-muted">
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-900/30 text-sm">
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.header} className="px-4 py-3 text-slate-200">
                  {column.accessor(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
