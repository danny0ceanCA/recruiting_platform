import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function SubmittedProfiles() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/students/");
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to fetch students");
        setStudents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p className="p-4">Loading…</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Submitted Profiles</h2>
      <ul className="space-y-2">
        {students.map((s) => (
          <li key={s.id} className="p-4 bg-white rounded shadow">
            <Link
              className="text-blue-600 hover:underline"
              to={`/profiles/${s.id}`}
            >
              {s.first_name} {s.last_name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
