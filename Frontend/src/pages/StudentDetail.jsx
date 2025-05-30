import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { API_URL } from "../api";

export default function StudentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API_URL}/students/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 401 || res.status === 403) {
          navigate("/", { replace: true });
          return;
        }
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to fetch student");
        setStudent(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) return <p className="p-4">Loading…</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;
  if (!student) return null;

  const fields = [
    { label: "Name", value: `${student.first_name} ${student.last_name}` },
    { label: "School", value: student.school },
    { label: "License Type", value: student.license_type },
    { label: "Job Goals", value: student.job_goals },
    { label: "Availability", value: student.availability },
    { label: "Transportation", value: student.transportation },
    { label: "Experience", value: student.experience },
    { label: "Soft Skills", value: student.soft_skills },
  ];

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <Link to="/profiles" className="text-blue-600 hover:underline">
        &larr; Back
      </Link>
      <Link
        to={`/profiles/${id}/edit`}
        className="text-blue-600 hover:underline block"
      >
        Edit Profile
      </Link>
      <h2 className="text-2xl font-bold">Student Detail</h2>
      <div className="bg-white p-4 rounded shadow">
        <ul className="space-y-1">
          {fields.map(
            (f) =>
              f.value && (
                <li key={f.label}>
                  <span className="font-semibold">{f.label}: </span>
                  {f.value}
                </li>
              )
          )}
          {student.ai_summary && (
            <li>
              <span className="font-semibold">AI Summary: </span>
              {student.ai_summary}
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}
