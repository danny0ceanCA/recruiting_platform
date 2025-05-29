import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function load() {
      if (!token) {
        navigate("/", { replace: true });
        return;
      }
      try {
        const meRes = await fetch("http://localhost:8000/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!meRes.ok) {
          navigate("/", { replace: true });
          return;
        }
        const me = await meRes.json();
        if (me.role !== "admin") {
          navigate("/dashboard", { replace: true });
          return;
        }
        const res = await fetch("http://localhost:8000/jobs/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to fetch jobs");
        setJobs(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [navigate, token]);

  if (loading) return <p>Loading…</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Job Postings</h2>
        <button
          onClick={() => navigate("/jobs/create")}
          className="px-3 py-1 bg-green-600 text-white rounded"
        >
          New Job
        </button>
      </div>
      {jobs.length === 0 ? (
        <p>No jobs available.</p>
      ) : (
        <ul className="space-y-2">
          {jobs.map((job) => (
            <li key={job.id} className="border p-2 rounded bg-white">
              <div className="flex justify-between">
                <div>
                  <p className="font-semibold">{job.title}</p>
                  <p>{job.description}</p>
                </div>
                <button
                  onClick={() => navigate(`/jobs/${job.id}/matches`)}
                  className="px-2 py-1 bg-blue-600 text-white rounded self-start"
                >
                  Match Now
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
