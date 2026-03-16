export default function HistoryTable({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="glass rounded-3xl p-6 shadow-glow overflow-x-auto">
      <h3 className="text-xl font-display mb-4">Threat History</h3>
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-ink/70">
            <th className="py-2 pr-4">Timestamp</th>
            <th className="py-2 pr-4">URL</th>
            <th className="py-2 pr-4">Risk</th>
          </tr>
        </thead>
        <tbody>
          {items.map((row) => (
            <tr key={row.id} className="border-t border-ink/10">
              <td className="py-2 pr-4">{row.timestamp}</td>
              <td className="py-2 pr-4">{row.url || "-"}</td>
              <td className="py-2 pr-4">{row.risk_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
