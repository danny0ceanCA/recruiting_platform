import React, { useState } from "react";

export default function StudentForm() {
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
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    setFormData((prev) => ({ ...prev, resume: file }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === "resume") {
        if (value) form.append("resume", value);
      } else {
        form.append(key, value);
      }
    });

    try {
      const res = await fetch("/students/start", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Submission failed");
      setMessage("Profile submitted successfully.");
      setFormData({
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
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          required
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
          required
          className="border border-gray-300 rounded px-3 py-2 w-full"
        />
        <input
          type="text"
          name="school"
          placeholder="School"
          value={formData.school}
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
      </div>

      <textarea
        name="job_goals"
        placeholder="Job Goals"
        value={formData.job_goals}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 w-full"
      />
      <textarea
        name="availability"
        placeholder="Availability"
        value={formData.availability}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 w-full"
      />
      <textarea
        name="transportation"
        placeholder="Transportation"
        value={formData.transportation}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 w-full"
      />
      <textarea
        name="experience"
        placeholder="Experience"
        value={formData.experience}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 w-full"
      />
      <textarea
        name="soft_skills"
        placeholder="Soft Skills"
        value={formData.soft_skills}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 w-full"
      />

      <input
        type="file"
        name="resume"
        accept=".pdf,.doc,.docx"
        onChange={handleFileChange}
      />

      <button
        type="submit"
        disabled={loading}
        className={`w-full py-2 text-white rounded ${
          loading ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Submitting…" : "Submit Profile"}
      </button>

      {message && <p className="text-center">{message}</p>}
    </form>
  );
}

