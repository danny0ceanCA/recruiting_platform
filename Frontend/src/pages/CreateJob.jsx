import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateJob() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [formData, setFormData] = useState({
    title: "",
    license_type: "",
    location: "",
    schedule: "",
    pay: "",
    description: "",
    tags: "",
    urgency: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function verifyAdmin() {
      if (!token) {
        navigate("/", { replace: true });
        return;
      }
      const res = await fetch("http://localhost:8000/users/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        navigate("/", { replace: true });
        return;
      }
      const me = await res.json();
      if (me.role !== "admin") navigate("/dashboard", { replace: true });
    }
    verifyAdmin();
  }, [navigate, token]);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = { ...formData };
      if (payload.pay === "") delete payload.pay;
      const res = await fetch("http://localhost:8000/jobs/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to create job");
      navigate("/jobs", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Create Job</h2>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-3 bg-white p-4 rounded shadow">
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={formData.title}
          onChange={handleChange}
          required
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="license_type"
          placeholder="License Type"
          value={formData.license_type}
          onChange={handleChange}
          required
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="location"
          placeholder="Location"
          value={formData.location}
          onChange={handleChange}
          required
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="schedule"
          placeholder="Schedule"
          value={formData.schedule}
          onChange={handleChange}
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="number"
          name="pay"
          placeholder="Pay"
          value={formData.pay}
          onChange={handleChange}
          step="0.01"
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <textarea
          name="description"
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="tags"
          placeholder="Tags"
          value={formData.tags}
          onChange={handleChange}
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="urgency"
          placeholder="Urgency"
          value={formData.urgency}
          onChange={handleChange}
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 text-white rounded ${
            loading ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Submitting…" : "Create Job"}
        </button>
      </form>
    </div>
  );
}
