import React from "react";
import StudentForm from "./StudentForm";

export default function StartProfile() {
  return (
    <div className="min-h-screen bg-transparent p-8">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded shadow">
        <h2 className="text-2xl font-bold mb-4">Start Student Profile</h2>
        <StudentForm />
      </div>
    </div>
  );
}