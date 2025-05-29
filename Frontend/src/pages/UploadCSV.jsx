import React, { useState } from "react";
import { API_URL } from "../api";

export default function UploadCsv() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setMessage("Please select a CSV file.");
    setLoading(true);
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_URL}/students/upload-csv`, {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      setMessage(`Created ${data.total} profiles.`);
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Upload CSV</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          {loading ? "Uploading…" : "Upload CSV"}
        </button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
}
