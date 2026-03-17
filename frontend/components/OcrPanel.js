export default function OcrPanel({ ocr }) {
  if (!ocr) return null;
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Screenshot OCR</h3>
      <div className="text-xs text-ink/60 mb-2">
        Status: {ocr.status}
      </div>
      {ocr.reason && (
        <div className="text-xs text-flare mb-2">
          Reason: {ocr.reason}
        </div>
      )}
      <p className="text-sm">{ocr.text || "No text recognized."}</p>
    </div>
  );
}
