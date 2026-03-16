export default function RecommendationList({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Recommended Actions</h3>
      <ul className="space-y-2 text-sm">
        {items.map((item, index) => (
          <li key={index} className="flex items-start gap-2">
            <span className="mt-1 h-2 w-2 rounded-full bg-ocean" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
