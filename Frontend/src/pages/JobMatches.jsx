import React, { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";

export default function JobMatches() {
  const { id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [matches, setMatches] = useState([]);
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      if (!token) {
        navigate("/", { replace: true });
        return;
      }
      try {
        const meRes = await fetch("http://localhost:8001/users/me", {
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

        const jobsRes = await fetch("http://localhost:8001/jobs/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const jobsData = await jobsRes.json();
        if (!jobsRes.ok) throw new Error(jobsData.detail || "Failed to fetch job");
        setJob(jobsData.find((j) => j.id === parseInt(id)) || null);

        const matchRes = await fetch(`http://localhost:8001/match-now/?job_id=${id}`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        });
        const matchData = await matchRes.json();
        if (!matchRes.ok) throw new Error(matchData.detail || "Failed to fetch matches");
        setMatches(matchData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id, navigate, token]);

  if (loading) return <p>Loading…</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <Link to="/jobs" className="text-blue-600 hover:underline">&larr; Back</Link>
      <h2 className="text-2xl font-bold">
        Matches for {job ? job.title : `Job ${id}`}
      </h2>
      {matches.length === 0 ? (
        <p>No matches found.</p>
      ) : (
        <ul className="space-y-2">
          {matches.map((m) => (
            <li key={m.student.id} className="border p-2 rounded bg-white">
              <p className="font-semibold">
                {m.student.first_name} {m.student.last_name} – Score {m.match_score}
              </p>
              <p>{m.student.school}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
