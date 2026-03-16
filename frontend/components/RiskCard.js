export default function RiskCard({ risk }) {
  if (!risk) return null;
  const level = risk.level || "SAFE";
  const color =
    level === "HIGH RISK" ? "bg-flare" : level === "SUSPICIOUS" ? "bg-sun" : "bg-moss";
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-display">Risk Score</h3>
        <span className={`risk-dot ${color}`} />
      </div>
      <div className="mt-4 text-5xl font-display">{risk.score}</div>
      <div className="mt-2 text-sm uppercase tracking-widest text-ink/60">{level}</div>
    </div>
  );
}
