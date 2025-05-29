import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  const schoolName = "Unitek Career Services";
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    async function checkRole() {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        const res = await fetch("http://localhost:8001/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) return;
        const data = await res.json();
        setIsAdmin(data.role === "admin");
      } catch {
        // ignore
      }
    }
    checkRole();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/", { replace: true });
  };

  const cardClasses =
    "flex-1 bg-white rounded-lg shadow p-6 text-center font-medium hover:shadow-lg transition";

  return (
    <div className="min-h-screen bg-transparent p-8">
      <div className="flex justify-between items-center max-w-4xl mx-auto mb-8">
        <h1 className="text-4xl font-bold">{schoolName}</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
        >
          Log Out
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <Link to="/start-profile" className={cardClasses}>
          Start Student Profile
        </Link>
        <Link to="/profiles" className={cardClasses}>
          View Submitted Profiles
        </Link>
        <Link to="/metrics" className={cardClasses}>
          Placement Metrics
        </Link>
        <Link to="/upload-csv" className={cardClasses}>
          Upload CSV
        </Link>
        {isAdmin && (
          <Link to="/jobs" className={cardClasses}>
            Manage Jobs
          </Link>
        )}
      </div>
    </div>
  );
}
