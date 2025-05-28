import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function StartProfile() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    license_type: "",
    school: "",
    job_goals: "",
    availability: "",
    transportation: "",
    experience: "",
    soft_skills: "",
    resume: null,
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  function handleChange(e) {
    const { name, value, files } = e.target;
    if (name === "resume") {
      setFormData(prev => ({ ...prev, resume: files[0] }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const form = new FormData();
    for (const [key, val] of Object.entries(formData)) {
      if (val) form.append(key, val);
    }

    try {
      const res = await fetch("/students/start", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to create profile");
      navigate("/profiles");
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  }

  const inputClass = "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none";

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Start Student Profile</h2>
      {message && <p className="text-red-600 mb-2">{message}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          className={inputClass}
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        <input
          className={inputClass}
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />
        <input
          className={inputClass}
          name="license_type"
          placeholder="License Type"
          value={formData.license_type}
          onChange={handleChange}
          required
        />
        <input
          className={inputClass}
          name="school"
          placeholder="School"
          value={formData.school}
          onChange={handleChange}
          required
        />
        <input
          className={inputClass}
          name="job_goals"
          placeholder="Job Goals"
          value={formData.job_goals}
          onChange={handleChange}
        />
        <input
          className={inputClass}
          name="availability"
          placeholder="Availability"
          value={formData.availability}
          onChange={handleChange}
        />
        <input
          className={inputClass}
          name="transportation"
          placeholder="Transportation"
          value={formData.transportation}
          onChange={handleChange}
        />
        <textarea
          className={inputClass}
          name="experience"
          placeholder="Experience"
          value={formData.experience}
          onChange={handleChange}
        />
        <textarea
          className={inputClass}
          name="soft_skills"
          placeholder="Soft Skills"
          value={formData.soft_skills}
          onChange={handleChange}
        />
        <input
          type="file"
          name="resume"
          onChange={handleChange}
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {loading ? "Submitting…" : "Submit"}
        </button>
      </form>
    </div>
  );
}
