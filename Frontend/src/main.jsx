// src/main.jsx
import React from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import "./index.css";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import StartProfile from "./pages/StartProfile";
import SubmittedProfiles from "./pages/SubmittedProfiles";
import StudentDetail from "./pages/StudentDetail";
import Metrics from "./pages/Metrics";
import UploadCsv from "./pages/UploadCsv";
import AdminPanel from "./pages/AdminPanel";
import Jobs from "./pages/Jobs";

// Simple guard component
function RequireAuth({ children }) {
  return localStorage.getItem("token")
    ? children
    : <Navigate to="/" replace />;
}

function AppRoutes() {
  const isLoggedIn = Boolean(localStorage.getItem("token"));

  return (
    <Routes>
      {/* Root: if logged in, send to dashboard; else show login */}
      <Route
        path="/"
        element={
          isLoggedIn
            ? <Navigate to="/dashboard" replace />
            : <Login />
        }
      />

      <Route
        path="/register"
        element={<Register />}
      />

      {/* All protected routes */}
      <Route
        path="/dashboard"
        element={
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        }
      />

      <Route
        path="/start-profile"
        element={
          <RequireAuth>
            <StartProfile />
          </RequireAuth>
        }
      />

      <Route
        path="/profiles"
        element={
          <RequireAuth>
            <SubmittedProfiles />
          </RequireAuth>
        }
      />

      {/* Detail view for a single student */}
      <Route
        path="/profiles/:id"
        element={
          <RequireAuth>
            <StudentDetail />
          </RequireAuth>
        }
      />

      <Route
        path="/metrics"
        element={
          <RequireAuth>
            <Metrics />
          </RequireAuth>
        }
      />

      <Route
        path="/upload-csv"
        element={
          <RequireAuth>
            <UploadCsv />
          </RequireAuth>
        }
      />

      <Route
        path="/admin"
        element={
          <RequireAuth>
            <AdminPanel />
          </RequireAuth>
        }
      />

      <Route
        path="/jobs"
        element={
          <RequireAuth>
            <Jobs />
          </RequireAuth>
        }
      />

      {/* Any unknown path → home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </React.StrictMode>
);
