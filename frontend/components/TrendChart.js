import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function TrendChart({ series }) {
  if (!series || series.length === 0) return null;
  const labels = series.map((item) => item.date);
  const chartData = {
    labels,
    datasets: [
      {
        label: "SAFE",
        data: series.map((item) => item["SAFE"] || 0),
        borderColor: "#5f9d61",
        backgroundColor: "rgba(95, 157, 97, 0.2)",
      },
      {
        label: "SUSPICIOUS",
        data: series.map((item) => item["SUSPICIOUS"] || 0),
        borderColor: "#f6bd60",
        backgroundColor: "rgba(246, 189, 96, 0.2)",
      },
      {
        label: "HIGH RISK",
        data: series.map((item) => item["HIGH RISK"] || 0),
        borderColor: "#f25c54",
        backgroundColor: "rgba(242, 92, 84, 0.2)",
      },
    ],
  };
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">Risk Trend Analytics</h3>
      <Line data={chartData} options={{ responsive: true }} />
    </div>
  );
}
