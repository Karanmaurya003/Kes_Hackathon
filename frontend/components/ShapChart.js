import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function ShapChart({ data, title }) {
  if (!data || data.length === 0) return null;
  const labels = data.map((d) => d.feature || d.token);
  const values = data.map((d) => Math.round(d.impact * 100) / 100);
  const chartData = {
    labels,
    datasets: [
      {
        label: "Impact",
        data: values,
        backgroundColor: "#0f4c5c",
      },
    ],
  };
  return (
    <div className="glass rounded-3xl p-6 shadow-glow">
      <h3 className="text-xl font-display mb-4">{title}</h3>
      <Bar data={chartData} options={{ responsive: true }} />
    </div>
  );
}
