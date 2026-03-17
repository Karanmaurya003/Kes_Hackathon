export default function NewsList({ items }) {
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Latest Phishing News</h3>
      {(!items || items.length === 0) && (
        <p className="text-sm text-ink/70">No news available yet.</p>
      )}
      <ul className="space-y-3 text-sm">
        {(items || []).map((item, idx) => (
          <li key={idx} className="border-b border-ink/10 pb-3 last:border-b-0">
            <div className="font-semibold">{item.title}</div>
            <div className="text-ink/60 text-xs">
              {item.source} · {item.date}
            </div>
            <div className="mt-1 text-ink/80">{item.summary}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
