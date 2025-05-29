import React, { useEffect, useState } from "react";

export default function Metrics() {
  const schoolName = "Unitek Career Services";
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const res = await fetch(
          `/reporting/overview?school=${encodeURIComponent(schoolName)}`
        );
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "Failed to fetch metrics");
        }
        setMetrics(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadMetrics();
  }, [schoolName]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Placement Metrics</h2>
      <p className="mb-2">Total Students: {metrics.total_students}</p>
      <p className="mb-4">Total Placed: {metrics.total_placed}</p>

      <p className="mb-2">Placement Rate: {metrics.placement_rate.toFixed(2)}%</p>
      <p className="mb-4">
        Avg. Time to Place: {metrics.average_time_to_place_days.toFixed(2)} days
      </p>

      <div>
        <h3 className="font-semibold">Interviews by Employer</h3>
        <ul className="list-disc ml-5">
          {Object.entries(metrics.interviews_by_employer).map(([employer, count]) => (
            <li key={employer}>{employer}: {count}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
