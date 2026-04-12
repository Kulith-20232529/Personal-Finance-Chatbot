import {
  Pie,
  Bar,
  Line
} from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";

ChartJS.register(
  ArcElement,
  BarElement,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

export default function Charts({ data }) {
  const labels = Object.keys(data.breakdown);
  const values = Object.values(data.breakdown);

  const historyLabels = Object.keys(data.history);
  const historyValues = Object.values(data.history);

  return (
    <div>
      <h3>Pie Chart</h3>
      <Pie data={{
        labels,
        datasets: [{ data: values }]
      }} />

      <h3>Bar Chart</h3>
      <Bar data={{
        labels,
        datasets: [{ data: values }]
      }} />

      <h3>Line Chart</h3>
      <Line data={{
        labels: historyLabels,
        datasets: [{ data: historyValues }]
      }} />
    </div>
  );
}