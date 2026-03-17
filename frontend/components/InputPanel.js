import { useState } from "react";

export default function InputPanel({ onAnalyze, loading }) {
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");
  const [screenshot, setScreenshot] = useState("");

  const handleFile = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setScreenshot(reader.result);
    reader.readAsDataURL(file);
  };

  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h2 className="text-2xl font-display mb-4">Threat Input</h2>
      <div className="space-y-4">
        <div>
          <label className="text-sm uppercase tracking-wide">URL</label>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="http://secure-paypal-verification.ru/login"
            className="mt-2 w-full rounded-xl border border-ink/10 bg-white p-3"
          />
        </div>
        <div>
          <label className="text-sm uppercase tracking-wide">Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Your bank account will be suspended. Verify immediately."
            rows={4}
            className="mt-2 w-full rounded-xl border border-ink/10 bg-white p-3"
          />
        </div>
        <div>
          <label className="text-sm uppercase tracking-wide">Screenshot</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFile}
            className="mt-2 w-full"
          />
          {screenshot && (
            <div className="mt-3 text-xs text-ink/60">Screenshot ready for OCR.</div>
          )}
        </div>
        {!url && !message && !screenshot && (
          <div className="text-xs text-flare">
            Add a URL, message, or screenshot to analyze.
          </div>
        )}
        <button
          onClick={() => onAnalyze({ url, message, screenshot })}
          disabled={loading || (!url && !message && !screenshot)}
          className="w-full rounded-xl bg-ocean px-4 py-3 text-white font-semibold hover:bg-ink transition"
        >
          {loading ? "Analyzing..." : "Analyze Threat"}
        </button>
      </div>
    </div>
  );
}
