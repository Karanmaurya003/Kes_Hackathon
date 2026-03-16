import { useEffect, useState } from "react";
import Head from "next/head";
import axios from "axios";
import InputPanel from "../components/InputPanel";
import RiskCard from "../components/RiskCard";
import RecommendationList from "../components/RecommendationList";
import ShapChart from "../components/ShapChart";
import HistoryTable from "../components/HistoryTable";
import TrendChart from "../components/TrendChart";
import HighlightedMessage from "../components/HighlightedMessage";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [trends, setTrends] = useState([]);

  const fetchHistory = async () => {
    const res = await axios.get(`${API_BASE}/history?limit=20`);
    setHistory(res.data.items || []);
  };

  const fetchTrends = async () => {
    const res = await axios.get(`${API_BASE}/trends?limit=120`);
    setTrends(res.data.series || []);
  };

  useEffect(() => {
    fetchHistory();
    fetchTrends();
  }, []);

  const handleAnalyze = async (payload) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/analyze`, payload);
      setResult(res.data);
      fetchHistory();
      fetchTrends();
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-hero-gradient">
      <Head>
        <title>PHISHLENS AI Dashboard</title>
        <link
          href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap"
          rel="stylesheet"
        />
      </Head>
      <header className="mx-auto max-w-6xl px-6 pt-12 pb-6">
        <div className="flex flex-col gap-4">
          <span className="uppercase text-xs tracking-[0.3em] text-ink/60">
            Explainable Multi-Layer Phishing Detection
          </span>
          <h1 className="text-4xl md:text-5xl font-display text-ink">
            PHISHLENS AI
          </h1>
          <p className="max-w-2xl text-ink/70">
            Multi-signal phishing defense combining URL intelligence, NLP detection,
            domain metadata, and explainable AI insights.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 pb-16 space-y-8">
        <section className="grid gap-6 md:grid-cols-[1.2fr_1fr]">
          <InputPanel onAnalyze={handleAnalyze} loading={loading} />
          <div className="space-y-6">
            <RiskCard risk={result?.risk} />
            <RecommendationList items={result?.recommendations || []} />
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <ShapChart
            data={result?.explainability?.url?.top_factors || []}
            title="URL Explainability"
          />
          <ShapChart
            data={result?.explainability?.message?.top_tokens || []}
            title="Message Explainability"
          />
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <HighlightedMessage
            message={result?.input?.message}
            highlights={result?.message_analysis?.highlight_terms}
          />
          <TrendChart series={trends} />
        </section>

        <section>
          <HistoryTable items={history} />
        </section>
      </main>
    </div>
  );
}
