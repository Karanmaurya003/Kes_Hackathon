const steps = [
  "Verify sender identity through a trusted channel.",
  "Never click links from unexpected or urgent messages.",
  "Check domains for subtle misspellings or unusual TLDs.",
  "Use multi-factor authentication on critical accounts.",
  "Report suspicious messages to your security team.",
];

export default function PreventionPanel() {
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Phishing Prevention Steps</h3>
      <ul className="space-y-2 text-sm">
        {steps.map((step, idx) => (
          <li key={idx} className="flex items-start gap-2">
            <span className="mt-1 h-2 w-2 rounded-full bg-ocean" />
            <span>{step}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
