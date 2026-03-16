export default function HighlightedMessage({ message, highlights }) {
  if (!message) return null;
  if (!highlights || highlights.length === 0) {
    return (
      <div className="glass rounded-3xl p-6 shadow-glow">
        <h3 className="text-xl font-display mb-4">Message Insight</h3>
        <p className="text-sm">{message}</p>
      </div>
    );
  }
  let rendered = message;
  highlights.forEach((word) => {
    const regex = new RegExp(`(${word})`, "gi");
    rendered = rendered.replace(regex, "**$1**");
  });
  const parts = rendered.split("**").map((part, idx) => {
    if (idx % 2 === 1) {
      return (
        <span key={idx} className="bg-sun/60 px-1 rounded">
          {part}
        </span>
      );
    }
    return <span key={idx}>{part}</span>;
  });
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Message Insight</h3>
      <p className="text-sm">{parts}</p>
    </div>
  );
}
