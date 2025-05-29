import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminPanel() {
  const [pendingUsers, setPendingUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchPending() {
      if (!token) {
        navigate("/", { replace: true });
        return;
      }
      try {
        // Verify role
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
        const res = await fetch("http://localhost:8000/admin/pending-users", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to fetch pending users");
        const data = await res.json();
        setPendingUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchPending();
  }, [navigate, token]);

  async function handleAction(id, action) {
    try {
      const res = await fetch(`http://localhost:8000/admin/${action}-user/${id}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Action failed");
      setPendingUsers((prev) => prev.filter((u) => u.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <p>Loading…</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow space-y-4">
      <h2 className="text-2xl font-bold">Pending Users</h2>
      {pendingUsers.length === 0 ? (
        <p>No pending users.</p>
      ) : (
        <ul className="space-y-2">
          {pendingUsers.map((user) => (
            <li
              key={user.id}
              className="flex justify-between items-center border p-2 rounded"
            >
              <span>{user.email}</span>
              <div className="space-x-2">
                <button
                  onClick={() => handleAction(user.id, "approve")}
                  className="px-2 py-1 bg-green-600 text-white rounded"
                >
                  Approve
                </button>
                <button
                  onClick={() => handleAction(user.id, "reject")}
                  className="px-2 py-1 bg-red-600 text-white rounded"
                >
                  Reject
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
